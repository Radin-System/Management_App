import time, paramiko
from functions.decorator import Connection_Required
from ._base import Connection

class SSH(Connection):
    def __init__(self,*,
        Host:str,
        Port:int,
        Username:str,
        Password:str,
        Encoding:str = 'utf-8',
        ) -> None:

        self.Host = Host
        self.Port = Port
        self.Username = Username
        self.Password = Password
        self.Encoding = Encoding

        self.Client = paramiko.SSHClient()
        self.Client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.History = ''
        self.Shell = None

    def Connect(self) -> None:
        self.Client.connect(
            hostname = self.Host,
            port     = self.Port,
            username = self.Username,
            password = self.Password,
            )
        self.Shell  = self.Client.invoke_shell(width=0,height=0)
        self.Excute_Mode = self.Check_Multi_Channel_Support()
        self.Banner = self.Client.get_transport().remote_version

    def Check_Multi_Channel_Support(self):
        try : 
            self.Client.invoke_shell().close()
            return True
        except paramiko.ChannelException:
            return False

    @Connection_Required
    def Receive(self) -> str:
        if self.Shell.recv_ready():
            return self.Shell.recv(65536).decode(self.Encoding)

    @Connection_Required
    def Send(self, Message:str, Wait:float = 0.5) -> str:
        if not Message.endswith('\n'): Message += '\n'
        if self.Excute_Mode:
            _ , Stdout , _ = self.Client.exec_command(Message)
            time.sleep(Wait)
            Response = Stdout.read().decode(self.Encoding)
            self.History += Message
            self.History += Response.replace('\r\n','\n').strip() if Response else ''
            return str(Response).replace('\r\n','\n').strip() if Response else ''
        else:
            if not Message.endswith('\n'): Message += '\n'
            self.Shell.send(Message)
            time.sleep(Wait)
            Response = self.Receive()
            self.History += Response.replace('\r\n','\n') if Response else ''
            return str(Response).strip() if Response else ''

    @Connection_Required
    def Disconnect(self) -> None :
        self.Shell = None
        self.Client.close()

    def Is_Connected(self) -> bool:
        return True if self.Client.get_transport() is not None and self.Client.get_transport().is_active() else False
