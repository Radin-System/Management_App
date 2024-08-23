import os, io, uuid, traceback, json
from datetime import datetime


ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Handle_Error(Error:Exception,*,
        Code:int=None, 
        Description:str=None,
        **KWargs
        ) -> str:

    # Ensure the directory exists
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    # Generate a unique filename
    Unique_UID = uuid.uuid4()
    File_Name = f'{Unique_UID}.{Code}.{ERROR_LOG_EXTENSION}'
    File_Path = os.path.join(ERROR_LOG_DIR, File_Name)

    # Extracting the traceback and putting it in a var
    Traceback_Str = io.StringIO()
    traceback.print_exception(type(Error), Error, Error.__traceback__, file=Traceback_Str)
    Traceback_Content = Traceback_Str.getvalue()

    Dict = dict(
        name = type(Error).__name__,
        description = str(Error) if Description is None else Description,
        code = int(Code),
        traceback = str(Traceback_Content),
        timestamp = str(datetime.now()),
        uid = str(Unique_UID),
        filename = str(File_Name),
        **KWargs
        )

    # Write the contents to the file
    with open(File_Path, 'w') as File:
        File.write(json.dumps(Dict))

    return Dict
