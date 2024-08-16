import uuid
from constants import Passkeys

def Create_Response(Message:dict|str,Status:str='Response',Code:int=200,**KWargs) -> dict:
    # Creating Base Response
    Response = dict(**KWargs)

    Response['status'] = Status
    Response['message'] = Message
    Response['code'] = Code

    return Response

def Create_Token(Passkey) -> dict|None:
    Detail = Passkeys.get(Passkey,None)
    if Passkeys:
        Uid = str(uuid.uuid4())
        return {Uid:Detail}
    else :
        return None