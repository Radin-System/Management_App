import time
import paramiko

from Class.decorator import Decorator
from . import Connection

class SSH(Connection) :
    def __init__(self,*, Host: str, Port: int, Username: str, Password: str) -> None:
        super().__init__(Host=Host, Port=Port, Username=Username, Password=Password)

        self.Client = paramiko.SSHClient()
        self.Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.Terminal = ''
        self.Shell = None
        self.Excute_Mode:bool = True

    def Connect(self) -> None :
        self.Client.connect(
            hostname = self.Host,
            port     = self.Port,
            username = self.Username,
            password = self.Password,
            )

        self.Shell  = self.Client.invoke_shell()
        self.Banner = self.Client.get_transport().remote_version

    @Decorator.Connection_Reqired
    def Receive(self) -> str :
        if self.Shell.recv_ready():
            return self.Shell.recv(65536).decode('utf-8')

    @Decorator.Connection_Reqired
    def Send(self, Message:str, Wait:float = 0.5) -> str:
        if not Message.endswith('\n'): Message += '\n'
        if self.Excute_Mode :
            _ , Stdout , _ = self.Client.exec_command(Message)
            time.sleep(Wait)
            Response = Stdout.read().decode('utf-8')
            self.Terminal += Message
            self.Terminal += Response.replace('\r\n','\n').strip() if Response else ''
            return str(Response).replace('\r\n','\n').strip() if Response else ''
        else :
            if not Message.endswith('\n') : Message += '\n'
            self.Shell.send(Message)
            time.sleep(Wait)
            Response = self.Receive()
            self.Terminal += Response.replace('\r\n','\n') if Response else ''
            return str(Response).strip() if Response else ''

    @Decorator.Connection_Reqired
    def Disconnect(self) -> None :
        self.Shell = None
        self.Client.close()

    def Is_Connected(self) -> bool:
        return True if self.Client.get_transport() is not None and self.Client.get_transport().is_active() else False