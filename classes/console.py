from classes.component import ComponentContainer as CC
from classes.component import SQLManager
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

        elif Command == 'reset_admin':
            SQL:SQLManager = CC.Get('MainSQLManager')
            Admin_User = SQL.Query(SQL.User, Detached=True, First=True, username='admin')
            if Admin_User:
                New_Password = input('Password : ')
                Admin_User.password = New_Password
                SQL.Update(Admin_User)
            else:
                Admin_User = SQL.User(username='admin', password='asd@1234', firstname_en='Administrator', firstname_fa='ادمین', admin=True)
                SQL.Create(Admin_User)
                print('New Admin User Created')
                print('Password: asd@1234')

        elif Command == 'reassign_dependencies':
            CC.Reassign_Dependencies()

        elif Command == 'start_all':
            CC.Start_All()

        elif Command == 'stop_all':
            CC.Stop_All()

        elif Command.startswith('start '):
            Service_Name = Command[len('start '):].strip()
            CC.Start(Service_Name)
            del Service_Name

        elif Command.startswith('stop '):
            Service_Name = Command[len('stop '):].strip()
            CC.Stop(Service_Name)
            del Service_Name

        elif Command == 'components':
            print(CC._Components)

        elif Command == 'processes':
            print(CC._Processes)

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
        for Name, Component in CC.Items():
            status = "Running" if Component.Is_Running() else "Stopped"
            print(f"{Name}: {status}")
