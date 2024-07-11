import time,paramiko
from Typing import Username,Password,IPv4,Port

class Device :
    def __init__(self,
            Host:IPv4,
            Port:Port,
            Username:Username,
            Password:Password
            ) -> None:
        
        self.Host     = Host
        self.Port     = Port
        self.Username = Username
        self.Password = Password

        self.Connection      = None
        self.Terminal        = ''
        self.Banner          = ''

    def SSH_Connect(self) -> None :
        self.Connection = paramiko.SSHClient()
        self.Connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.Connection.connect(
            hostname = self.Host,
            port     = self.Port,
            username = self.Username,
            password = self.Password,
            )
        
        self.Shell  = self.Connection.invoke_shell()
        self.Banner = self.Connection.get_transport().remote_version

    def Connected(self) -> bool:
        return True if self.Connection.get_transport() is not None and self.Connection.get_transport().is_active() else False

    def Receive(self) -> str :
        if self.Connected() :
            if self.Shell.recv_ready():
                return self.Shell.recv(65536).decode('utf-8')
        else : raise ConnectionError('Not Connected to the Device')

    def Execute(self, Message:str, Wait:float = 0.5) -> str:
        if not Message.endswith('\n'): Message += '\n'
        if self.Connected():
            _ , Stdout , _ = self.Connection.exec_command(Message)
            time.sleep(Wait)
            Response = Stdout.read().decode('utf-8')
            self.Terminal += Message
            self.Terminal += Response.replace('\r\n','\n').strip() if Response else ''
            return str(Response).replace('\r\n','\n').strip() if Response else ''
        else : raise ConnectionError('Not Connected to the Device')

    def Send(self, Message:str, Wait:float = 0.5) -> str:
        if not Message.endswith('\n') : Message += '\n'
        if self.Connected() :
            self.Shell.send(Message)
            time.sleep(Wait)
            Response = self.Receive()
            self.Terminal += Response.replace('\r\n','\n') if Response else ''
            return str(Response).strip() if Response else ''
        else : raise ConnectionError('Not Connected to the Device')

    def Get_Command_Prompt(self) -> str :
        return self.Send(' ')

    def Disconnect(self) -> None :
        self.Shell.close()
        self.Connection.close()
        self.Connection = None
