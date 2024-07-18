from . import Device

class Mikrotik(Device):
    def __init__(self,*Args,**Kwargs) -> None:
        super().__init__(*Args,**Kwargs)

    def Get_Hostname(self) -> str:
        return self.Connection.Send('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str:
        return self.Connection.Send('export',15)