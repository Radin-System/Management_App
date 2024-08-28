from classes.component import ComponentContainer
from constant import CONSOLE_WELCOME, CONSOLE_HELP

class Console:
    def __init__(self,*,
        Startup:list = None,
        Shutdown:list = None,
        ) -> None:

        self.Startup = Startup or []
        self.Shutdown = Shutdown or []

        self.Running = False

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        print(CONSOLE_WELCOME)

        ## Handling Startup Commands
        [self.Handle_Command(Startup_Command) for Startup_Command in self.Startup]

        while self.Is_Running():
            try:
                Command = input("> ").strip()
                self.Handle_Command(Command)
            except KeyboardInterrupt:
                self._exit()
            except Exception as e:
                print(f"Error: {e}")

    def Stop(self) -> None:

        [self.Handle_Command(Shutdown_Command) for Shutdown_Command in self.Shutdown]

        self.Running = False

    def Handle_Command(self, Command:str) -> None:
        if Command == 'exit':
            self.Stop()

        elif Command == 'help':
            print(CONSOLE_HELP)

        elif Command == 'reassign_dependencies':
            ComponentContainer.Reassign_Dependencies()

        elif Command == 'start_all':
            ComponentContainer.Start_All()

        elif Command == 'stop_all':
            ComponentContainer.Stop_All()

        elif Command.startswith('start '):
            Service_Name = Command[len('start '):].strip()
            ComponentContainer.Start(Service_Name)
            del Service_Name

        elif Command.startswith('stop '):
            Service_Name = Command[len('stop '):].strip()
            ComponentContainer.Stop(Service_Name)
            del Service_Name

        elif Command == 'components':
            print(ComponentContainer._Components)

        elif Command == 'processes':
            print(ComponentContainer._Processes)

        elif Command == 'status':
            self._print_status()

        elif Command == '':
            pass

        else:
            print(f"\nUnknown command: {Command}")

    def _exit(self) -> None:
        print("\nShutting down the console...")
        self.Running = False

    def _print_status(self) -> None:
        for Name, Component in ComponentContainer.Items():
            status = "Running" if Component.Is_Running() else "Stopped"
            print(f"{Name}: {status}")
