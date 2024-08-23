from flask import jsonify

ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Create_Response(Message:dict|str,Status:str='Response',Code:int=200,**KWargs) -> dict:
    # Creating Base Response
    Response = dict(**KWargs)

    Response['status'] = Status
    Response['message'] = Message
    Response['code'] = Code

    return jsonify(Response), Code
