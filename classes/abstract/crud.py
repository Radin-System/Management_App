from abc import abstractmethod

class CRUD:
    @abstractmethod
    def Query() -> None:
        ...

    @abstractmethod
    def Create() -> None:
        ...

    @abstractmethod
    def Update() -> None:
        ...
    
    @abstractmethod
    def Delete() -> None:
        ...