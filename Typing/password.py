

class Password :
    def __init__(self , Input : str ) -> None : 
        self.Input    = Input
        self.Crypted  = None
        self.MD5      = None
        self.Raw      = None
        self.Method   = None
        self.Score    = 0

        if   Validate.MD5(self.Input)     : self.Method = 'MD5'
        elif Validate.Crypted(self.Input) : self.Method = 'Crypted'
        else                              : self.Method = 'Raw' 

        if   self.Method == 'MD5'     :
            self.MD5     = self.Input
            self.Crypted = ''
            self.Raw     = ''
        elif self.Method == 'Raw'     : 
            self.MD5     = Crypto.MD5(self.Input)
            self.Crypted = Crypto.Encrypt(self.Input)
            self.Raw     = self.Input
        elif self.Method == 'Crypted' :
            self.MD5     = Crypto.MD5(Crypto.Decrypt(self.Input.encode('utf-8')))
            self.Crypted = self.Input.encode('utf-8')
            self.Raw     = Crypto.Decrypt(self.Input)

        self.Validate()

    def Validate(self) -> None :
        if any(char.islower()        for char in self.Raw) : self.Score += 1
        if any(char.isupper()        for char in self.Raw) : self.Score += 1
        if any(char.isdigit()        for char in self.Raw) : self.Score += 1
        if any(char in SPECIAL_CHARS for char in self.Raw) : self.Score += 1
        self.Valid = bool(self.Method == 'MD5' or (self.Score >= 3 and len(self.Raw) >= 7))

    def __str__ (self) -> str :
        return '****'
    
    def __bool__ (self) -> bool :
        return self.Valid