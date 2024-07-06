import time,paramiko
from Global.Class.Auth    import User,Password
from Global.Class.Network import Hostname,IPv4,Port

class Device :
    def __init__(self,Hostname:Hostname,ManagementIP:IPv4,ManagementPort:Port,Username:User,Password:Password) -> None :
        self.Hostname       = Hostname
        self.ManagementIP   = ManagementIP
        self.ManagementPort = ManagementPort
        self.Username       = Username
        self.Password       = Password

        self.Connection_Type = None
        self.Connection      = None
        self.Terminal        = ''
        self.Banner          = ''

    def Create_SSH_Client(self) -> None :
        self.Connection_Type = 'SSH'
        self.Connection      = paramiko.SSHClient()
        self.Connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def Create_Telnet_Client(self) -> None :
        raise DeprecationWarning('Telnet is Depricated')

    def Connect(self) -> None :
        if self.Connection_Type == 'SSH' :
            ## This Part Will Connect to device and get the shell , it will authenticate
            self.Connection.connect(hostname=self.ManagementIP.IPv4,port=self.ManagementPort.Number,username=self.Username.Username,password=self.Password.Raw)
            self.Shell  = self.Connection.invoke_shell()
            self.Banner = self.Connection.get_transport().remote_version
        if self.Connection_Type == 'Telnet' :
            raise DeprecationWarning('Telnet is Depricated')

    def Connected(self) -> bool :
        if   self.Connection_Type == 'SSH'    : return True if self.Connection.get_transport() is not None and self.Connection.get_transport().is_active() else False
        elif self.Connection_Type == 'Telnet' : return False
        else : return False

    def Receive(self) -> str :
        if self.Connected() :
            if self.Connection_Type == 'SSH' :
                if self.Shell.recv_ready() :
                    return self.Shell.recv(65536).decode('utf-8')
            else : return None
        else : raise ConnectionError('Not Connected to the Device')

    def Execute(self,Message:str,Wait:float=0.5) -> str :
        if not Message.endswith('\n') : Message += '\n'
        if self.Connected() :
            if self.Connection_Type == 'SSH' :
                _ , Stdout , _ = self.Connection.exec_command(Message)
                time.sleep(Wait)
                Response = Stdout.read().decode('utf-8')
                self.Terminal += Message
                self.Terminal += Response.replace('\r\n','\n').strip() if Response else ''
                return str(Response).replace('\r\n','\n').strip() if Response else ''
            if self.Connection_Type == 'Telnet' : 
                raise DeprecationWarning('Telnet is Depricated')
        else : raise ConnectionError('Not Connected to the Device')

    def Send(self,Message:str,Wait:float=0.5) -> str :
        if not Message.endswith('\n') : Message += '\n'
        if self.Connected() :
            if self.Connection_Type == 'SSH' :
                self.Shell.send(Message)
                time.sleep(Wait)
                Response = self.Receive()
                self.Terminal += Response.replace('\r\n','\n') if Response else ''
                return str(Response).strip() if Response else ''
            if self.Connection_Type == 'Telnet' : 
                raise DeprecationWarning('Telnet is Depricated')
        else : raise ConnectionError('Not Connected to the Device')

    def Get_Command_Prompt(self) -> str :
        return self.Send(' ')

    def Disconnect (self) -> None :
        if self.Connection_Type == 'SSH' and self.Connected() :
            self.Shell.close()
            self.Connection.close()
            self.Connection = None
        elif self.Connection_Type == 'Telnet' and self.Connected() :
            raise DeprecationWarning('Telnet is Depricated')
