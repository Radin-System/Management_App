from classes.component import ComponentContainer as CC
from classes.component import SQLManager
from constant import CONSOLE_WELCOME, CONSOLE_HELP
from functions.errorhandler import Handle_Error
from getpass import getpass

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
                Detail = Handle_Error(e)
                print(f"{str(type(e).__name__)}: {e}")
                print(f'Error UID: {Detail.get('uid','No UID')}')

    def Stop(self) -> None:

        [self.Handle_Command(Shutdown_Command) for Shutdown_Command in self.Shutdown]

        self.Running = False

    def Handle_Command(self, Command:str) -> None:
        if Command == 'exit':
            self.Stop()

        elif Command == 'help':
            print(CONSOLE_HELP)

        elif Command == 'reset_admin':
            New_Password = getpass('Password : ')
            Confirm_Password = getpass('Confirm  : ')
            if not New_Password == Confirm_Password:
                raise ValueError('Provided passwords do not match')

            SQL:SQLManager = CC.Get('MainSQLManager')
            Admin_User = SQL.Query(SQL.User, Detached=True, First=True, username='admin')
            if Admin_User:
                Admin_User.password = New_Password
                SQL.Update(Admin_User)

            else:
                Admin_User = SQL.User(username='admin', password=New_Password, firstname_en='Administrator', firstname_fa='ادمین', admin=True)
                SQL.Create(Admin_User)
                print('New Admin User Created')

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
