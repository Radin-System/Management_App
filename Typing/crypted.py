class Crypted :
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        if isinstance(self.Input,str)   : self.Crypted = self.Input.encode('utf-8')
        if isinstance(self.Input,bytes) : self.Crypted = self.Input
        self.Validate()
        if not self.Valid : self.Crypted = b''

    def Validate(self) -> None:
        self.Valid = Validate.Crypted(self.Crypted)

    def __str__(self) -> str:
        return self.Input
    
    def __bool__ (self) -> bool:
        return self.Valid
