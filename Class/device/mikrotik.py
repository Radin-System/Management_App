from . import Device

class Mikrotik(Device):
    def __init__(self, Name, *, Host: str, Port: int, Username: str, Password: str) -> None:
        super().__init__(Name, Host=Host, Port=Port, Username=Username, Password=Password)

    def Get_Hostname(self) -> str:
        return self.Connection.Send('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str:
        return self.Connection.Send('export',15)