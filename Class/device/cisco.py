from Class.connection import Connection as Con
from . import Device

class Cisco(Device):
    def __init__(self, Name:str,*,
            Enable:str
            ) -> None:

        super().__init__(Name)

        self.Enable = Enable

    def Prepare_Connection(self) -> None:
        self.Set_State('privileged')
        self.Connection.Send('terminal width 0')
        self.Connection.Send('terminal length 0')
        self.Connection.Send('terminal no monitor')

    def Get_Command_Prompt(self) -> str :
        return self.Connection.Send(' ')

    def Get_Hostname(self) -> str:
        self.Set_State('privileged')
        Command_Prompt = self.Get_Command_Prompt()
        return Command_Prompt.replace('#','').strip()

    def Get_Config(self, Mode:str='full') -> str:
        self.Set_State('privileged')
        return self.Connection.Send(f'show running-config {Mode}',5.5)

    def State(self) -> str:
        Command_Prompt = self.Get_Command_Prompt()
        if '(config)#' in Command_Prompt : return 'configure'
        if '(config-'  in Command_Prompt : return 'interface'
        if '#'         in Command_Prompt : return 'privileged'
        if '>'         in Command_Prompt : return 'userEXEC'
        raise ValueError(f'Unable to parse current state from command prompt : {Command_Prompt}')

    def Set_State(self, New_State:str) -> None:
        Current_State = self.State()
        if Current_State == 'userEXEC'   and New_State == 'privileged' : self.Connection.Send('enable') ; self.Connection.Send(self.Enable) ; return
        if Current_State == 'privileged' and New_State == 'userEXEC'   : self.Connection.Send('disable') ; return
        if Current_State == 'privileged' and New_State == 'configure'  : self.Connection.Send('configure terminal') ; return
        if Current_State == 'configure'  and New_State == 'privileged' : self.Connection.Send('exit') ; return

        if Current_State == 'interface'  and New_State != 'interface'  : self.Connection.Send('exit') ; self.Set_State(New_State) ; return

        if Current_State == 'userEXEC'   and New_State == 'configure'  : self.Set_State('privileged') ; self.Set_State('configure') ; return
        if Current_State == 'configure'  and New_State == 'userEXEC'   : self.Set_State('privileged') ; self.Set_State('userEXEC') ; return
        if Current_State == New_State                                  : pass # Do Nothing
        else : raise Exception(f'Invalid States : Current_State={Current_State} , New_State={New_State}')