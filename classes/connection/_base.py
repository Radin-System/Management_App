from abc import abstractmethod
from typing import Self

class Connection:

    @abstractmethod
    def Connect(self) -> None :
        ...

    @abstractmethod
    def Receive(self) -> str :
        ...

    @abstractmethod
    def Send(self, Message:str, Wait:float = 0.2) -> str:
        ...

    @abstractmethod
    def Disconnect(self) -> None :
        ...

    @abstractmethod
    def Is_Connected(self) -> bool:
        ...

    def __bool__(self) -> bool :
        return self.Is_Connected()

    def __enter__(self) -> Self :
        self.Connect()
        return self

    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Disconnect()

    def __str__(self) -> str :
        return f'<Connection :{self.__class__.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*args,**Kwargs)'