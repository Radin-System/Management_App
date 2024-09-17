from typing import Any, Dict

from ._base import Component

from classes.abstract.container import Container
from classes.exception import ContainerError

class ComponentContainer(Container):
    _Components: Dict[str, Component] = {}

    @classmethod
    def Register(cls, Name: str, Component: Component) -> None:
        if Name not in cls._Components:
            cls._Components[Name] = Component
        else:
            raise ContainerError.Exists(f'Component Already exists: {Name}\n Try another name')

    @classmethod
    def Get(cls, Name:str, Default:Any = None) -> Component:
        Result = cls._Components.get(Name, Default)
        if Result is not None: 
            return Result
        else : 
            raise ContainerError.NotFound(f'The requested Component not found: {Name}')

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
        Component.Start()

    @classmethod
    def Stop(cls, Name: str) -> None:
        Component = cls.Get(Name)
        Component.Stop()

    @classmethod
    def Start_All(cls) -> None:
        for Name in cls._Components.keys():
            cls.Start(Name)

    @classmethod
    def Stop_All(cls) -> None:
        for Name in cls._Components.keys():
            cls.Stop(Name)