import os, io, uuid, traceback, copy, json
from datetime import datetime
from flask import jsonify, request

ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Create_Response(Message:dict|str,Status:str='Response',Code:int=200,**KWargs) -> dict:
    # Creating Base Response
    Response = dict(**KWargs)

    Response['status'] = Status
    Response['message'] = Message
    Response['code'] = Code

    return Response

def Create_Error_File(Error_Object:Exception, Status_Code:int ,Response:dict) -> str|None:
    # Ensuring that we dont change the response
    Response_Copy = copy.deepcopy(Response)

    # Ensure the directory exists
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    # Generate a unique filename
    Unique_UID = uuid.uuid4()
    Unique_Filename = f'{Unique_UID}.{Status_Code}.{ERROR_LOG_EXTENSION}'
    File_Path = os.path.join(ERROR_LOG_DIR, Unique_Filename)

    # Extracting the traceback and putting it in a var
    Traceback_Str = io.StringIO()
    traceback.print_exception(type(Error_Object), Error_Object, Error_Object.__traceback__, file=Traceback_Str)
    Traceback_Content = Traceback_Str.getvalue()

    # Adding additinal data to file
    Response_Copy['traceback'] = str(Traceback_Content)
    Response_Copy['message']['uid'] = str(Unique_UID)
    Response_Copy['message']['url'] = str(request.url)
    Response_Copy['message']['form'] = str(request.form)

    # Write the contents to the file
    with open(File_Path, 'w') as File:
        File.write(json.dumps(Response_Copy))

    return Unique_UID

def Handle_API_Error(Error_Object:Exception, Status_Code:int, Description:str=None):
    Data = {
        'description':Error_Object.description if Description is None else Description,
        'timestamp': str(datetime.now()),
        
        'uid': None,
        'url':'NotImplementedError', # Implement a way to give access to some clients to see the full log
        'form':'NotImplementedError', # Implement a way to give access to some clients to see the full log
        }
    Response = Create_Response(Data, 'Error', Status_Code, traceback='NotImplementedError')

    Uid = Create_Error_File(Error_Object, Status_Code, Response)

    Response['message']['uid'] = Uid

    return jsonify(Response), Status_Code