class Addr :
    def __init__(self , Input : str) -> None :

        self.Input = Input.strip()

        if ':' in Input :
            i , j = Input.split(':',1)
            self.IP   = IPv4(i.strip())
            self.Port = Port(j.strip())
        else :
            self.IP   = ''
            self.Port = ''

        self.Validate()

    def Validate (self) -> None :
        self.Valid = True if self.IP and self.Port else False

    def __str__ (self) -> str :
        return f'{self.IP.IPv4}:{self.Port.Number}' if self.Valid else self.Input

    def __bool__ (self) -> bool :
        return self.Valid
