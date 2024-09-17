from abc import abstractmethod

class Container:
    @abstractmethod
    def Register():
        ...

    @abstractmethod
    def Get():
        ...

    @abstractmethod
    def Remove():
        ...

    @abstractmethod
    def Reassign_Dependencies():
        ...