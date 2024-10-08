from classes.enum import RespondHeader
from classes.enum.console import InputType
from classes.exception import ConsoleError
from ._base import Console

COMMAND_REGISTRY = {}

def Register_Command(name:str):
    def decorator(func):
        COMMAND_REGISTRY[name] = func
        return func
    return decorator

@Register_Command('help')
def help(Self:Console, Command_Name:str=None, *Args:str):
    """
      Prints out the help for that commands
      or all off the commands if there is no
      "Commands_Name" specified

      args:
        Command_Name -Optional
    """
    if Command_Name:
        Command_Function = COMMAND_REGISTRY.get(Command_Name)

        if Command_Function:
            # Print the docstring of the specific command
            Doc = Command_Function.__doc__ or "No documentation available."
            print(f"  > {Command_Name}{Doc}")

        else:
            raise ConsoleError.Command.NotFound(f'Command not found: {Command_Name}')

    else:
        # No specific command requested, print general help and all commands
        Self.Output("Commands:")

        for Command_Name, Command_Function in COMMAND_REGISTRY.items():
            Doc = Command_Function.__doc__ or "No documentation available."
            print(f"  > {Command_Name}{Doc}")

@Register_Command('reset_admin')
def reset_admin(Self:Console, *Args:str):
    """
      Resets the Admin user password
      if there is none Admin users it creates one
      the Admin user is not deletable !

      args:
        None
    """
    from classes.component import ComponentContainer as CC
    from classes.component import SQLManager

    New_Password = Self.Input(f'{RespondHeader.Input.value} Password : ', InputType.Password)
    Confirm_Password = Self.Input(f'{RespondHeader.Input.value} Confirm  : ', InputType.Password)

    SQL:SQLManager = CC.Get('Main_SQLManager')
    Admin_User = SQL.Query(SQL.User, Detached=True, First=True, username='admin')
    if Admin_User:
        Admin_User.reset_password(
            New = New_Password,
            Confirm = Confirm_Password,
            Expire = False
            )

        SQL.Update(Admin_User)

    else:
        Admin_User = SQL.User(username='admin', password=New_Password, firstname_en='Administrator', firstname_fa='ادمین', admin=True, deletable=False)
        SQL.Create(Admin_User)
        Self.Output('New Admin User Created')

@Register_Command('reassign_dependencies')
def reassign_dependencies(Self:Console, *Args:str):
    """
      Reassigns dependencies of all components

      args:
        None
    """
    from classes.component import ComponentContainer as CC

    CC.Reassign_Dependencies()

@Register_Command('start_all')
def start_all(Self:Console, *Args:str):
    """
      args:
        None

      Starts all of the components
    """
    from classes.component import ComponentContainer as CC
    
    CC.Start_All()

@Register_Command('stop_all')
def stop_all(Self:Console, *Args:str):
    """
      Stops all of the components

      args:
        None
    """
    from classes.component import ComponentContainer as CC
    
    CC.Stop_All()

@Register_Command('start')
def start(Self:Console, Component_Name:str=None, *Args:str):
    """
      Starts the specified Component

      args:
        Component_Name
    """
    from classes.component import ComponentContainer as CC

    if not Component_Name:
        ConsoleError.Command.MissingArg('No componnent specified')

    CC.Start(Component_Name)

@Register_Command('stop')
def stop(Self:Console, Component_Name, *Args:str):
    """
      Stops the specified Component

      args:
        Component_Name
    """
    from classes.component import ComponentContainer as CC

    if not Component_Name:
        ConsoleError.Command.MissingArg('No componnent specified')

    CC.Stop(Component_Name)


@Register_Command('components')
def components(Self:Console, *Args:str):
    """
      Prints components names

      args:
        None
    """
    from classes.component import ComponentContainer as CC

    for Component_Name in CC._Components.keys():
        Self.Output(Component_Name)

@Register_Command('tools')
def tools(Self:Console, *Args:str):
    """
      Prints tools names

      args:
        None
    """
    from classes.tool import ToolContainer as TC

    for Tool_Name in TC._Tools.keys():
        Self.Output(Tool_Name)

@Register_Command('status')
def status(Self:Console, Component_Name=None, *Args:str):
    """
      Prints the Component status if there is
      no "Component_Name" it will print all of them

      args:
        Component_Name -optional
    """
    from classes.component import ComponentContainer as CC

    if not Component_Name:
        for Key, Component in CC._Components.items():
            Self.Output(f'{Key}: {'Running' if Component.Is_Running() else 'Stopped'}')
    
    else :
        Component = CC.Get(Component_Name)
        Self.Output(f'{Component_Name}: {'Running' if Component.Is_Running() else 'Stopped'}')

@Register_Command('exit')
def exit(Self:Console, Code:str='0', *Args:str):
    """
      exits the program with 0 code
      if "Code" not specified

      args:
        Code -optional
    """
    from classes.component import ComponentContainer as CC

    if Code.isdigit():
        Code:int = int(Code)

    Self.Output(Code)
    Self.Stop(Code)