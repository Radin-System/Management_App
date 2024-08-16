import time
from scapy.all import Raw,sniff,sendp,Ether
from functions.decorator import Connection_Required
from ._base import Connection

class MacTelnet(Connection):
    def __init__(self,*,
            Interface:str,
            Source:str,
            Destination:str,
            Encoding:str='utf-8'
            ) -> None:

        self.Source = Source
        self.Interface = Interface
        self.Destination = Destination
        self.Encoding = Encoding

        self.History = ''
        self.connected = False
        self.shell = None

    def Connect(self) -> None:
        # Create Ethernet frame for MAC-Telnet request
        eth = Ether(src=self.Source, dst=self.Destination, type=0x8888)  # MikroTik MAC-Telnet uses EtherType 0x8888

        # Empty payload for connection initiation
        payload = b''

        # Send the frame
        sendp(eth/payload, iface=self.Interface)

        # Wait for a response
        response = sniff(iface=self.Interface, count=1, timeout=5)
        if response:
            self.connected = True
            self.shell = response[0]  # Simplified example, handle response appropriately

    @Connection_Required
    def Receive(self) -> str:
        if self.shell:
            response = sniff(iface=self.Interface, count=1, timeout=5)
            if response:
                return response[0].load.decode(self.Encoding)

    @Connection_Required
    def Send(self, message: str, wait: float = 0.5) -> str:
        if not message.endswith('\n'):
            message += '\n'
        
        # Create Ethernet frame with the command
        eth = Ether(src=self.Source, dst=self.Destination, type=0x8888) / Raw(load=message.encode(self.Encoding))
        
        sendp(eth, iface=self.Interface)
        time.sleep(wait)
        response = self.Receive()
        self.History += response.replace('\r\n', '\n') if response else ''
        return str(response).strip() if response else ''

    @Connection_Required
    def Disconnect(self) -> None:
        self.shell = None
        self.connected = False

    def Is_Connected(self) -> bool:
        return self.connected
