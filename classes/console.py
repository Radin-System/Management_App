from classes.component import ComponentContainer

class Console:
    def __init__(self) -> None:
        self.Running = False

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        print("\nConsole is now running. Type 'exit' to quit.")
        while self.Is_Running():
            try:
                command = input("> ").strip()
                self.Handle_Command(command)
            except KeyboardInterrupt:
                self._exit()
            except Exception as e:
                print(f"Error: {e}")

    def Stop(self) -> None:
        self.Running = False

    def Handle_Command(self, Command:str) -> None:
        if Command == 'exit':
            self.Stop()

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
