from Class.device  import Device
from Class.Auth    import Username , Password
from Class.Network import Hostname, IPv4 , Port

class Cisco(Device):
    def __init__(self,*,
            Host:IPv4,
            Port:Port,
            Username:Username,
            Password:Password,
            Enable:Password,
            )->None:

        super().__init__(Host,Port,Username,Password)
        self.Enable = Enable

    def Prepare_Terminal(self) -> None:
        if self.Connected():
            self.Set_State('privileged')
            self.Send('terminal width 0')
            self.Send('terminal length 0')
            self.Send('terminal no monitor')

    def Set_State(self, State) -> None:
        CurrentState = self.State()
        if CurrentState and State:
            if CurrentState == 'userEXEC'   and State == 'privileged' : self.Send('enable') ; self.Send(self.Enable.Raw) ; return
            if CurrentState == 'privileged' and State == 'userEXEC'   : self.Send('disable') ; return
            if CurrentState == 'privileged' and State == 'configure'  : self.Send('configure terminal') ; return
            if CurrentState == 'configure'  and State == 'privileged' : self.Send('exit') ; return

            if CurrentState == 'interface'  and State != 'interface'  : self.Send('exit') ; self.Set_State(State) ; return

            if CurrentState == 'userEXEC'   and State == 'configure'  : self.Set_State('privileged') ; self.Set_State('configure') ; return
            if CurrentState == 'configure'  and State == 'userEXEC'   : self.Set_State('privileged') ; self.Set_State('userEXEC') ; return
            if CurrentState == State                                  : pass # Do Nothing
            else : raise Exception(f'State {State} is not a valid Cisco State' )
        else : raise Exception(f'Invalid States : CurrentState={CurrentState} , State={State}')

    def State(self) -> str:
        Command_Prompt = self.Get_Command_Prompt()
        if '(config)#' in Command_Prompt : return 'configure'
        if '(config-'  in Command_Prompt : return 'interface'
        if '#'         in Command_Prompt : return 'privileged'
        if '>'         in Command_Prompt : return 'userEXEC'
        raise ValueError(f'Command_Prompt does not have correct char at the end : {Command_Prompt}')

    def Get_RunningConfig(self, Mode:str = 'full') -> str:
        self.Set_State('privileged')
        return self.Send(f'show running-config {Mode}',5.5)

    def Get_Hostname(self) -> str:
        self.Set_State('privileged')
        Command_Prompt = self.Get_Command_Prompt()
        return Command_Prompt.replace('#','').strip()