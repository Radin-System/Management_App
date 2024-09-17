from typing import Any, Dict

from classes.exception import ContainerError

from ._base import Tool

class ToolContainer:
    _Tools: Dict[str, Tool] = {}

    @classmethod
    def Register(cls, Name:str, Tool:Tool) -> None:
        if Name not in cls._Tools:
            cls._Tools[Name] = Tool
        else:
            raise ContainerError.Exists(f'Tool Already exists: {Name}\nTry another name')

    @classmethod
    def Get(cls, Name:str, Default:Any = None) -> Tool:
        Result = cls._Tools.get(Name, Default)
        if Result is not None: 
            return Result
        else : 
            raise ContainerError.NotFound(f'The requested Tool not found: {Name}')

    @classmethod
    def Remove(cls, Name: str) -> Tool:
        return cls._Tools.pop(Name, None)

    @classmethod
    def Reassign_Dependencies(cls) -> None:
        for Tool in cls._Tools.values():
            Tool.Init_Dependancy()
