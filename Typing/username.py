from . import Validate

class Username :
    def __init__(self , Input : str) -> None :
        self.Input = Input
        self.Validate()
        self.Username = self.Input if self.Valid else ''

    def Validate(self) -> None :
        self.Valid = bool(Validate.User(self.Input))

    def __str__ (self) -> str :
        return self.Username if self.Valid else self.Input
    
    def __bool__ (self) -> bool :
        return self.Valid
