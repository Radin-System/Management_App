from typing import Callable

class Component :

    Running:bool = None
    Logger:Callable = print

    def Start_Actions(self) -> None :
        raise NotImplementedError('Please provide an action for starting the componnet')

    def Stop_Actions(self) -> None:
        raise NotImplementedError('Please provide an action for stopping the componnet')

    def Is_Running(self) -> bool:
        return self.Running

    def Start(self) -> None:
        self.Running = True
        self.Start_Actions()

    def Stop(self) -> None:
        self.Running = False
        self.Stop_Actions()

    def __enter__(self) -> None :
        self.Start()

    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Stop()

    def __bool__(self) -> bool :
        return self.Running

    def __str__(self) -> str :
        return f'<Component :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'
