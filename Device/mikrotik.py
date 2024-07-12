from Class.device  import Device
from Typing.username import Username
from Typing.password import Password
from Typing.ipv4 import IPv4
from Typing.port import Port

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