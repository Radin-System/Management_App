class Email:
    def __init__(self , Input : str) -> None : 
        self.Input = Input.strip()
        self.User   = ''
        self.Domain = ''

        if '@' in self.Input :
            Username , DomainName = self.Input.split('@',1)
            self.User   = Username(Username)
            self.Domain = Domain(DomainName)

        self.Validate()
        self.Email         = self.Input if self.Valid else ''
        self.userPrincipal = self.Email

    def Validate(self) -> None :
        self.Valid = bool( self.User and self.Domain and Validate.Email(self.Input)) 

    def __str__ (self) -> str :
        return f'{self.User.Username}@{self.Domain.Domain}' if self.Valid else self.Input
    
    def __bool__ (self) -> bool :
        return self.Valid
