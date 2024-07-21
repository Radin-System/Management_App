from Class.device import Device

class Interface:
    
    Running:bool = None
    Enabeld:bool = None
    Addresses:list[str] = []
    Mac_Address:str = None
    Description:str = None

    def __init__(self,Detail:dict) -> None:
        self.Detail = Detail
    
    def __bool__(self) -> bool:
        ...
    
    def __str__(self) -> str :
        return f'<Interface :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(**Kwargs)'

class Ethernet(Interface):
    ...

class VLan(Interface):
    ...

class WireGuard(Interface):
    ...

    class Peer(Interface):
        ...

    Peers:list[Peer] = []