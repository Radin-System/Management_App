from Class.connection import Connection

class Device :
    def __init__(self,Name:str) -> None:
        self.Name = Name

        self.Logger = print
        self.Connection:Connection = None

    def Connect(self,via:Connection,*,
            Host:str,
            Port:int,
            Username:str,
            Password:str
            ) -> None :

        self.Connection = via(Host=Host,Port=Port,Username=Username,Password=Password)
        self.Connection_Type = self.Connection.__class__.__name__

    def __str__(self) -> str :
        return f'<Component :{self.Name}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.Name}",*Args,**Kwargs)'
