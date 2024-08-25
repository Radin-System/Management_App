from typing import Callable, Any, Self
from classes.exception import ServiceError

class Service:

    Running:bool = False

    def __init__(self, Name:str) -> None:
        self.Name = Name
        self.Running = False

        ServiceContainer.Register(Name, self)
        self.Init_Dependancy()
        self.Init_Config()

    def Init_Dependancy(self) -> None:
        from .logger import Logger
        from classes.component.config import Config
        self.Logger:Logger = ServiceContainer.Get('MainLogger', print)
        self.Config:Config = ServiceContainer.Get('MainConfig')

    def Init_Config(self) -> None:
        raise NotImplementedError(f'Please provide an action for configing the service: {self.Name}')

    def Start_Actions(self) -> None :
        raise NotImplementedError(f'Please provide an action for starting the service: {self.Name}')

    def Stop_Actions(self) -> None:
        raise NotImplementedError(f'Please provide an action for stopping the service: {self.Name}')

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        self.Start_Actions()

    def Stop(self) -> None:
        self.Running = False
        self.Stop_Actions()

    def __enter__(self) -> Self :
        self.Start()
        return self
    
    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Stop()

    def __bool__(self) -> bool :
        return self.Running

    def __str__(self) -> str :
        return f'<Component :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'

class ServiceContainer:
    _Services:dict[str, Service] = {}

    @classmethod
    def Register(cls, Name:str, Service:Service) -> None:
        Result = cls._Services.get(Name, None)
        if Result is None:
            cls._Services[Name] = Service
        else:
            raise ServiceError.Exists('Service Already exists: {Name}\n Try another name')

    @classmethod
    def Get(cls, Name:str, Default:Any = None) -> Service:
        Result = cls._Services.get(Name, Default)
        if Result is not None: 
            return Result
        else : 
            raise ServiceError.NotFound(f'The requested service not found: {Name}')

    @classmethod
    def Remove(cls, Name:str) -> Service:
        return cls._Services.pop(Name, None)

    @classmethod
    def Start(cls, Name:str) -> None:
        cls.Get(Name).Start()

    @classmethod
    def Stop(cls, Name:str) -> None:
        cls.Get(Name).Stop()

    @classmethod
    def Start_All(cls) -> None:
        for Server in cls._Services.values():
            Server.Start()

    @classmethod
    def Stop_All(cls) -> None:
        for Server in cls._Services.values():
            Server.Stop()

    @classmethod
    def Items(cls) -> tuple[list[str], list[Service]]:
        return cls._Services.items()

__all__ = [
    'Service',
    'ServiceContainer',
]