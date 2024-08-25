import time
from typing import Any, Dict, Tuple
import multiprocessing
import threading

from classes.exception import ServiceError

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
        raise NotImplementedError(f'Please provide an action for configuring the service: {self.Name}')

    def Start_Actions(self) -> None:
        raise NotImplementedError(f'Please provide an action for starting the service: {self.Name}')

    def Stop_Actions(self) -> None:
        raise NotImplementedError(f'Please provide an action for stopping the service: {self.Name}')

    def Is_Running(self) -> bool:
        return self.Running

    def Loop(self) -> None:
        while self.Is_Running():
            time.sleep(0.2)

    def Start(self) -> None:
        self.Running = True
        
        self.Logger(f'Starting the Service: {self.Name}')
        self.Start_Actions()
        self.Loop()

    def Stop(self) -> None:
        self.Logger(f'Stopping the Service: {self.Name}')
        self.Running = False
        self.Stop_Actions()

    def __enter__(self) -> 'Component':
        self.Start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.Stop()

    def __bool__(self) -> bool:
        return self.Running

    def __str__(self) -> str:
        return f'<Component :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.Name})'

    def _run_service(self) -> None:
        self.Start()

class ComponentContainer:
    _Components: Dict[str, Component] = {}
    _Processes: Dict[str, Any] = {}  # To keep track of processes or threads

    @classmethod
    def Register(cls, Name: str, Service: Component) -> None:
        if Name not in cls._Components:
            cls._Components[Name] = Service
        else:
            raise ServiceError.Exists(f'Service Already exists: {Name}\n Try another name')

    @classmethod
    def Get(cls, Name:str, Default:Any = None) -> Component:
        Result = cls._Components.get(Name, Default)
        if Result is not None: 
            return Result
        else : 
            raise ServiceError.NotFound(f'The requested service not found: {Name}')

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
            Process = multiprocessing.Process(target=Component._run_service)
            Process.start()
            cls._Processes[Name] = Process

        elif Component.Process_Type == 'Thread':
            Component.Logger(f'Creating Thread for {Name}', 'debug')
            Thread = threading.Thread(target=Component._run_service)
            Thread.start()
            cls._Processes[Name] = Thread

        elif Component.Process_Type == 'Static':
            Component.Start()

        else:
            raise ValueError(f'Unknown Process_Type: {Component.Process_Type}')

    @classmethod
    def Stop(cls, Name: str) -> None:
        service = cls.Get(Name)
        service.Stop()
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