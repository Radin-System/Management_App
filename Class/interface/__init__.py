from Class.device import Device

class Interface:
    def __bool__(self) -> bool:
        ...
    
    def __str__(self) -> str :
        return f'<Infrastructure :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'

class WireGuard(Interface):
    class Peer:
        def __init__(self,Name:str,*,
            Number:int,
            Public_Key:str,
            Private_Key:str=None,
            Endpoint:str=None,
            Endpoint_Port:int=None,
            Allowed_Address:str='0.0.0.0/0',
            Preshared_Key:str=None,
            Persistent_Keepalive:str=None,
            ) -> None:

            self.Name = Name
            self.Number = Number
            self.Public_Key = Public_Key
            self.Private_Key = Private_Key
            self.Endpoint = Endpoint
            self.Endpoint_Port = Endpoint_Port
            self.Allowed_Address = Allowed_Address
            self.Preshared_Key = Preshared_Key
            self.Persistent_Keepalive = Persistent_Keepalive
        
        def Update_string(self,**Kwargs) -> str :
            return f'interface/peer set {self.Number} '
    
    Peers:list[Peer] = []

    def __init__(self,Name:str,*,
        Number:int,
        Listen_Port:int,
        Private_key:str,
        Public_Key:str,
        ) -> None:
        
        self.Name = Name
        self.Number = Number
        self.Listen_Port = Listen_Port
        self.Private_key = Private_key
        self.Public_Key = Public_Key
