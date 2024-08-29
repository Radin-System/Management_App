import sys, time, importlib
from typing import Callable

from constant import CONSOLE_BANNER, CONSOLE_WELCOME
from functions.errorhandler import Handle_Error

def Load_Command(Command_Name) -> Callable:
    Module = importlib.import_module('.commands', package='classes.console')
    Command_Function = getattr(Module, Command_Name)

    return Command_Function

class Console:
    def __init__(self, *, Startup: list = None, Shutdown: list = None) -> None:
        self.Startup = Startup or []
        self.Shutdown = Shutdown or []
        self.Running = False

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        print(CONSOLE_BANNER)

        [self.Handle_Command(cmd) for cmd in self.Startup]
        time.sleep(1)
        print(CONSOLE_WELCOME)

        while self.Is_Running():
            try:
                command = input("> ").strip()
                self.Handle_Command(command)
            except KeyboardInterrupt:
                self._exit()
            except Exception as e:

                detail = Handle_Error(e)
                print(f"{str(type(e).__name__)}: {e}")
                print(f'Error UID: {detail.get("uid", "No UID")}')

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

        Command_Function = Load_Command(Cmd)
        if Command_Function:
            Command_Function(self, *args)

        else:
            print(f"\nUnknown command: {Cmd}")

    def Respond(self, Text:str) -> None:
        for Line in Text.splitlines():
            print('-', Line)

    def _exit(self) -> None:
        print("\nShutting down the console...")
        self.Stop()