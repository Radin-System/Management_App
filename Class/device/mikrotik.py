from . import Device

class Mikrotik(Device):
    def __init__(self, Name:str) -> None:
        super().__init__(Name)

    def Get_Hostname(self) -> str:
        return self.Connection.Send('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str:
        return self.Connection.Send('export',15)