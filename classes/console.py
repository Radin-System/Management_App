from classes.component import ComponentContainer

WELCOME:str = r'''
/'\_/`\                                                            ( )_ 
|     |   _ _   ___     _ _    __     __    ___ ___     __    ___  | ,_)
| (_) | /'_` )/' _ `\ /'_` ) /'_ `\ /'__`\/' _ ` _ `\ /'__`\/' _ `\| |  
| | | |( (_| || ( ) |( (_| |( (_) |(  ___/| ( ) ( ) |(  ___/| ( ) || |_ 
(_) (_)`\__,_)(_) (_)`\__,_)`\__  |`\____)(_) (_) (_)`\____)(_) (_)`\__)
                            ( )_) |                                     
                             \___/'                                     
                       _____  ___    ___                                
                      (  _  )(  _`\ (  _`\                              
    ______  ______    | (_) || |_) )| |_) )    ______  ______           
   (______)(______)   |  _  || ,__/'| ,__/'   (______)(______)          
                      | | | || |    | |                                 
                      (_) (_)(_)    (_)                                 
                                                                        
- Welcome to the application console
- For get commands detail type:
    > help
'''

HELP:str = '''
- Commands:
  > help
      Shows help

  > status
      Shows the status of Components

  > components
      prints the componnets in dict format

  > processes
      prints the processes list in dict format

  > start <Componnet Name>
      starts the mentiond componnet

  > stop <Componnet Name>
      stops the mentiond componnet

  > start_all
      Starts all of the componnets

  > stop_all
      Stops all of the componnets

  > exit or Control-C
      Exits the console
'''

class Console:
    def __init__(self) -> None:
        self.Running = False

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        print(WELCOME)
        while self.Is_Running():
            try:
                Command = input("> ").strip()
                self.Handle_Command(Command)
            except KeyboardInterrupt:
                self._exit()
            except Exception as e:
                print(f"Error: {e}")

    def Stop(self) -> None:
        self.Running = False

    def Handle_Command(self, Command:str) -> None:
        if Command == 'exit':
            self.Stop()

        elif Command == 'help':
            print(HELP)

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
