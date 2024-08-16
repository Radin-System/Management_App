import uuid
from constants import Passkeys

def Create_Token(Passkey) -> dict|None:
    Detail = Passkeys.get(Passkey,None)
    if Passkeys:
        Uid = str(uuid.uuid4())
        return {Uid:Detail}
    else :
        return None