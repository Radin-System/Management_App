from abc import abstractmethod

class Component:
    def __init__(self, Name: str) -> None:
        self.Name = Name

        self.Running = False

        from classes.component import ComponentContainer
        ComponentContainer.Register(Name, self)

        self.Init_Dependancy()
        self.Init_Config()

    def Init_Dependancy(self) -> None:
        from classes.tool import ToolContainer

        from classes.tool import Logger
        from classes.tool import Config
        self.Logger:Logger = ToolContainer.Get(f'{self.Name}_Logger', ToolContainer.Get('Main_Logger', print))
        self.Config:Config = ToolContainer.Get(f'{self.Name}_Config', ToolContainer.Get('Main_Config'))

    @abstractmethod
    def Init_Config(self):
        ...

    @abstractmethod
    def Start_Actions(self) -> None:
        ...

    @abstractmethod
    def Stop_Actions(self) -> None:
        ...

    def Is_Running(self) -> bool:
        return self.Running

    @abstractmethod
    def Loop(self) -> None:
        ...

    def Start(self) -> None:
        self.Running = True
        self.Logger(f'Starting the component: {self.Name}')
        self.Start_Actions()
        self.Loop()

    def Stop(self) -> None:
        self.Logger(f'Stopping the component: {self.Name}')
        self.Running = False
        self.Stop_Actions()

    def __enter__(self) -> 'Component':
        self.Start()
        return self

    def __exit__(self, Exc_Type, Exc_Value, Traceback) -> None:
        self.Stop()

    def __bool__(self) -> bool:
        return self.Running

    def __str__(self) -> str:
        return f'<Component :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.Name})'

    def _Run_Component(self) -> None:
        self.Start()
