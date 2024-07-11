from Class.device  import Device
from Class.Auth    import Username , Password
from Class.Network import Hostname, IPv4 , Port

class Mikrotik(Device):
    def __init__(self,*,
            Host:IPv4,
            Port:Port,
            Username:Username,
            Password:Password,
            ) -> None:

        super().__init__(Host,Port,Username,Password)

    def Get_Hostname(self) -> str:
        return Device.Execute('system identity print').replace('name:','').strip()

    def Get_Export(self) -> str:
        Output = self.Execute('export',15)
        return Output