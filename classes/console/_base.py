import sys, time, importlib
from typing import Any, Callable

from classes.enum.console import RespondHeader, InputType
from classes.exception import ConsoleError
from constant import CONSOLE_BANNER, CONSOLE_WELCOME
from functions.errorhandler import Handle_Error

class Console:
    def __init__(self,*, 
            Startup:list = None, 
            Shutdown:list = None
            ) -> None:

        self.Startup = Startup or []
        self.Shutdown = Shutdown or []
        self.Running = False

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        self.Output(CONSOLE_BANNER, RespondHeader.Nothing)

        [self.Handle_Command(cmd) for cmd in self.Startup]
        time.sleep(1)

        self.Output(CONSOLE_WELCOME, RespondHeader.Info)

        while self.Is_Running():
            try:
                Command = self.Input(f'{RespondHeader.Terminal.value} ').strip()
                self.Handle_Command(Command)

            except KeyboardInterrupt:
                self._exit()

            except Exception as e:
                detail = Handle_Error(e)
                self.Output(f"{str(type(e).__name__)}: {e}", RespondHeader.Error)
                self.Output(f'Error UID: {detail.get("uid", "No UID")}', RespondHeader.Error)

    def Stop(self,Code:int=0) -> None:
        self.Running = False
        [self.Handle_Command(cmd) for cmd in self.Shutdown]
        
        if Code: sys.exit(Code)

    def Handle_Command(self, Command: str) -> None:
        parts = Command.split()
        if not parts:
            return

        Cmd = parts[0]
        args = parts[1:]

        Command_Function = self.Load_Command(Cmd)
        if Command_Function:
            try:
                Command_Function(self, *args)

            except KeyboardInterrupt:
                self.Output('Intrupted by User', RespondHeader.Space)

        else:
            self.Output(f"Unknown command: {Cmd}", RespondHeader.Error)

    @staticmethod
    def Load_Command(Command_Name) -> Callable:
        Module = importlib.import_module('.commands', package=__package__)
        Command_Function = getattr(Module, Command_Name, None)
        if not Command_Function:
            raise ConsoleError.Command.NotFound(f'Command not found: {Command_Name}')

        return Command_Function

    def Input(self, Prompt, Method=InputType.Raw) -> str:
        return Method.value(Prompt).strip()

    def Output(self, Text:Any, Type=RespondHeader.Info) -> None:
        Text:str = str(Text)
        for Line in Text.splitlines():
            print(Type.value, Line)

    def _exit(self) -> None:
        self.Output("Shutting down the console...")
        self.Stop()