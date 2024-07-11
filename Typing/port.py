class Port :
    def __init__(self , Input : str) -> None :
        """Input Example : 80/HTTP , 576/TCP , 0/ICMP , LDAP"""
        self.Input = Input
        if '/' in self.Input :
            self.Number , self.Protocol = self.Input.strip().split('/',1)
            self.Protocol = self.Protocol.upper()
            try    : self.Number = int(self.Number)
            except : self.Number = 0
        else :
            self.Number   = Get.Port_Number(self.Input)
            self.Protocol = self.Input if Validate.Port(self.Number) else ''

        self.Validate()

        if self.Valid :
            self.Type          = Get.Port_Type(self.Protocol)
            self.Protocol      = self.Protocol
            self.Well_Khown    = Validate.WellKhown(self.Number)
            self.Default       = Validate.DefaultProtocol(self.Number , self.Protocol)

    def Validate (self) -> None :
        if   self.Number == 0 and self.Protocol.upper() == 'ICMP'            : self.Valid = True
        elif self.Number != 0 and self.Protocol.upper() == 'ICMP'            : self.Valid = False
        elif Validate.Port(self.Number) and Validate.Protocol(self.Protocol) : self.Valid = True
        else                                                                 : self.Valid = False

    def __str__ (self) -> str :
        return f'{self.Number}/{self.Protocol}' if self.Valid else self.Input
    
    def __bool__ (self) -> str :
        return self.Valid