from .                    import Device
from Global.Class.Auth    import Username , Password
from Global.Class.Network import Hostname, IPv4 , Port

class Mikrotik (Device):
    def __init__(self,
                 Hostname:Hostname,
                 ManagementIP:IPv4,
                 ManagementPort:Port,
                 Username:Username,
                 Password:Password,)->None:
        self.Logger          = print
        super().__init__(Hostname,ManagementIP,ManagementPort,Username,Password)

    def State(self) -> str :
        return ''

    def Set_State(self , State : str) -> None :
        CurrentState = self.State()
        if CurrentState and State :
            pass

    def Get_Hostname(self) -> str :
        return Device.Execute('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str :
        Output = self.Execute('export',15)
        return Output