import time
from typing import Any, Dict, Tuple
import multiprocessing
import threading

from classes.exception import ComponentError

class Component:
    def __init__(self, Name: str) -> None:
        self.Name = Name

        self.Running = False
        self.Process_Type:str = 'Thread'

        ComponentContainer.Register(Name, self)
        self.Init_Dependancy()
        self.Init_Config()

    def Init_Dependancy(self) -> None:
        from .logger import Logger
        from classes.component.config import Config
        self.Logger: Logger = ComponentContainer.Get('MainLogger', print)
        self.Config: Config = ComponentContainer.Get('MainConfig')

    def Init_Config(self) -> None:
        raise NotImplementedError(f'Please provide an action for configuring the component: {self.Name}')

    def Start_Actions(self) -> None:
        raise NotImplementedError(f'Please provide an action for starting the component: {self.Name}')

    def Stop_Actions(self) -> None:
        raise NotImplementedError(f'Please provide an action for stopping the component: {self.Name}')

    def Is_Running(self) -> bool:
        return self.Running

    def Loop(self) -> None:
        raise NotImplementedError(f'Please provide an action for Looping the component: {self.Name}')

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

class ComponentContainer:
    _Components: Dict[str, Component] = {}
    _Processes: Dict[str, Any] = {}  # To keep track of processes or threads

    @classmethod
    def Register(cls, Name: str, Component: Component) -> None:
        if Name not in cls._Components:
            cls._Components[Name] = Component
        else:
            raise ComponentError.Exists(f'Component Already exists: {Name}\n Try another name')

    @classmethod
    def Get(cls, Name:str, Default:Any = None) -> Component:
        Result = cls._Components.get(Name, Default)
        if Result is not None: 
            return Result
        else : 
            raise ComponentError.NotFound(f'The requested Component not found: {Name}')

    @classmethod
    def Remove(cls, Name: str) -> Component:
        return cls._Components.pop(Name, None)

    @classmethod
    def Reassign_Dependencies(cls) -> None:
        for Server in cls._Components.values():
            Server.Init_Dependancy()

    @classmethod
    def Start(cls, Name: str) -> None:
        Component = cls.Get(Name)
        Component.Logger(f'Process type of {Name}: {Component.Process_Type}', 'debug')

        if Component.Process_Type == 'Process':
            Component.Logger(f'Creating Proccess for {Name}', 'debug')
            Process = multiprocessing.Process(target=Component._Run_Component)
            Process.start()
            cls._Processes[Name] = Process

        elif Component.Process_Type == 'Thread':
            Component.Logger(f'Creating Thread for {Name}', 'debug')
            Thread = threading.Thread(target=Component._Run_Component)
            Thread.start()
            cls._Processes[Name] = Thread

        elif Component.Process_Type == 'Static':
            Component.Start()

        else:
            raise ValueError(f'Unknown Process_Type: {Component.Process_Type}')

    @classmethod
    def Stop(cls, Name: str) -> None:
        component = cls.Get(Name)
        component.Stop()
        if Name in cls._Processes:
            process_or_thread = cls._Processes.get(Name)
            process_or_thread:threading.Thread|multiprocessing.Process

            process_or_thread.join()

    @classmethod
    def Start_All(cls) -> None:
        for Name in cls._Components.keys():
            cls.Start(Name)

    @classmethod
    def Stop_All(cls) -> None:
        for Name in cls._Components.keys():
            cls.Stop(Name)

    @classmethod
    def Items(cls) -> Tuple[list[str], list[Component]]:
        return cls._Components.items()

__all__ = [
    'Component',
    'ComponentContainer',
]