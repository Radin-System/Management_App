class MD5 :
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        self.Validate()
        if self.Valid : self.MD5 = self.Input

    def Validate(self) -> None:
        self.Valid = Validate.MD5(self.Input)

    def __str__(self) -> str:
        return self.Input
    
    def __bool__(self) -> bool:
        return self.Valid
