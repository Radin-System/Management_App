ERROR_LOG_DIR = '.errors/'
ERROR_LOG_EXTENSION = 'json'

def Create_API_Response(Message:dict|str,Status:str='Response',Code:int=200,**KWargs) -> dict:
    # Creating Base Response
    API_Response = dict(**KWargs)

    API_Response['status'] = Status
    API_Response['message'] = Message
    API_Response['code'] = Code

    return API_Response
