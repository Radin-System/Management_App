from Class.connection import Connection

class Device :
    def __init__(self,Name,*,
            Host:str,
            Port:int,
            Username:str,
            Password:str,
            ) -> None:

        self.Name = Name
        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password

        self.Logger = print
        self.Connection:Connection = None

    def Connect(self,via:Connection) -> None :
        self.Connection = via(
            Host=self.Host,
            Port=self.Port,
            Username=self.Username,
            Password=self.Password,
        )

    def __str__(self) -> str :
        return f'<Component :{self.Name}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.Name}",*Args,**Kwargs)'
