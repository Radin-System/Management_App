from Class.connection import Connection as Con

class Device :
    
    Logger = print
    Hostname:str = None
    Domain:str = None
    Connection:Con = None
    Interfaces:list = []
    Services:list = []

    def __init__(self,Name) -> None:
        self.Name = Name

    def Connect(self,via:Con,*,
            Host:str,
            Port:int,
            Username:str,
            Password:str
            ) -> None :

        self.Connection = via(Host=Host,Port=Port,Username=Username,Password=Password)
        self.Connection_Type = self.Connection.__class__.__name__

    def __str__(self) -> str :
        return f'<Device :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'
