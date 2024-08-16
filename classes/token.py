from constants import Passkeys
import hashlib

class Token :
    _Active_Tokens = []

    def __init__(self,Passkey,SSID) -> None:
        self.Passkey = Passkey
        self.SSID = SSID

    def Get_Detail(self) -> None:
        Detail = Passkeys.get(self.Passkey,None)

    def Validate(self,Provided_Token,SSID) -> bool:
        Generated_Token = Token.Generate_Token(SSID)
        return Provided_Token == Generated_Token

    def Generate_Token(Passkey,SSID) -> str:
        Algoritm_String = f'ASDP{Passkey}KH+#t{SSID}'.encode('utf-8')
        Hasshed_ALG = hashlib.sha256(Algoritm_String).hexdigest()
        return Hasshed_ALG