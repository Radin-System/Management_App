import time, socket
from .base import Connection
from Function.decorator import Connection_Required

class TcpSocket(Connection):
    def __init__(self,*,
        Host:str,
        Port:int,
        Username:str,
        Password:str,
        Encoding:str = 'utf-8',
        ) -> None :

        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password
        self.Encoding = Encoding

        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.History = ''
        self.Shell = None
        self.Excute_Mode:bool = True

    def Connect(self) -> None :
        self.Client.connect((self.Host, self.Port))

    @Connection_Required
    def Receive(self) -> str :
        return self.Client.recv(65536).decode(self.Encoding)

    @Connection_Required
    def Send(self, Message:str, Wait:float = 0.2) -> str:
        self.Client.sendall(Message.encode())
        time.sleep(Wait)
        return self.Receive()

    @Connection_Required
    def Disconnect(self) -> None :
        self.Client.close()

    def Is_Connected(self) -> bool:
        try: self.Client.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        except BlockingIOError: return True
        except ConnectionResetError: return False
        return True
