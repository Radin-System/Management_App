import threading,socket,time
from ._base import Component

class AMIManager(Component):
    def __init__(self,Name:str) -> None:
        super().__init__(Name)

        self.Client_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ActionId = 0

        self.Connected     = None
        self.Authenticated = None

    def Init_Config(self) -> None:
        self.Host         = self.Config.Get('AMIMANAGER', 'host')
        self.Port         = self.Config.Get('AMIMANAGER', 'port')
        self.Usename      = self.Config.Get('AMIMANAGER', 'username')
        self.Password     = self.Config.Get('AMIMANAGER', 'password')
        self.Whitelist    = self.Config.Get('AMIMANAGER', 'event_whitelist_csv')
        self.Timeout      = self.Config.Get('AMIMANAGER', 'timeout')
        self.Max_ActionID = self.Config.Get('AMIMANAGER', 'max_action_id')

    def Connect(self) -> None :
        if not self.Connected :
            self.Client_Socket.connect((self.Host, self.Port))
            self.Connected = True
            self.Receiver_Thread = threading.Thread(target=self.Receiver)
            self.Receiver_Thread.start()

    def Disconnect(self) -> None :
        if self.Connected :
            self.Client_Socket.close()
            self.Connected = False
            self.Logger('Disconnected')

    def Login(self) -> None :
        if not self.Authenticated :
            Response = self.Send_Action('Login', Username = self.Usename, Secret = self.Password)
            if Response :
                if 'Success' in Response.get('Response') :
                    self.Authenticated = True
                    self.Logger('Login Success')
                elif 'Error' in Response.get('Response') :
                    self.Authenticated = False
                    self.Logger('Login Faild')
                    raise ConnectionError(f'Unable to Log in to the AMI Server : {Response.get('Message')}')

    def Logoff(self) -> None :
        if self.Authenticated :
            Response = self.Send_Action('Logoff')
            self.Authenticated = False
            if Response :
                if 'Goodbye' in Response.get('Response') : self.Logger('Loged off Succsessfuly')
                else : self.Logger('Unsuccsessful Logoff - Still changing flag to logedoff')
                
    def Event_Parser(self, Event:str) -> dict | None:
        Lines = Event.strip().split('\r\n')
        Operation = {}
        for Line in Lines:
            if 'Asterisk Call Manager' in Line : continue
            key, value = Line.split(':', 1)
            Operation[key.lstrip()] = value.lstrip().split(',') if ',' in value else value.lstrip()
        return Operation
    
    def Receiver(self) -> None:
        Buffer = b''
        while self.Running and self.Connected:
            Data = self.Client_Socket.recv(2048)
            Buffer += Data
            while b'\r\n\r\n' in Buffer :
                Raw_Operation , Buffer = Buffer.split(b'\r\n\r\n', 1)
                Operation = self.Event_Parser(Raw_Operation.decode())
                if 'Event' in Operation.keys():
                    if Operation.get('Event') in self.Whitelist :
                        New_Event = threading.Thread(target=self.Handel_Event , args=(Operation,) )
                        New_Event.start()

    def Handel_Event(self, Event:dict) -> None:
        try :
            self.Logger(f'New Event : {Event.get('Event')}')
            Functions = __import__(name = '_Globals.Functions.AMI.Responses' , fromlist=[Event.get('Event')])
            Function = getattr(Functions , Event.get('Event'))
            Function(self , Event)
        except ImportError    : self.Logger('Action Not Found')
        except Exception as e : self.Logger(f'Unable to react to the Event : {e}')

    def Send_Action(self, Act, **kwargs) -> dict | None:
        if     self.ActionId > self.Max_ActionID : self.ActionId = 1
        else : self.ActionId += 1
        Action = f'Action: {Act}\r\n'
        Action += f'ActionID: {self.ActionId}\r\n'
        for key, value in kwargs.items() : Action += f'{key}: {value}\r\n'
        Action += '\r\n'
        self.Client_Socket.sendall(Action.encode())
        self.Logger(f'Action Sent : {Act} - {self.ActionId}')
        Start = time.time()
        while time.time() - Start < self.Timeout :
            Response = next((r for r in self.Responses if r.get('ActionID') == str(self.ActionId)), None)
            if Response:
                self.Logger(f'Response of Action-{self.ActionId} : {Response}')
                return Response
        else : self.Logger(f'Timeout waiting for response with ActionID : {self.ActionId}')

    def Start_Actions(self):
        self.Connect()
        self.Login()

    def Stop_Actions(self):
        self.Logoff()
        self.Disconnect()