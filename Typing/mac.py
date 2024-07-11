class MAC :
    def __init__(self , Input : str) -> None :
        
        Strip = '.-:,'
        self.Input = Input.strip()
        
        for Item in Strip : self.Mac = self.Input.replace(Item , '')
        
        self.Validate()

        if self.Valid :
            self.Hex    = self.Mac.upper()
            self.Dotted = '.'.join([self.Mac.lower()[i:i+4] for i in range(0,12,4)])
            self.Dubble = ':'.join([self.Mac.upper()[i:i+2] for i in range(0,12,2)])
        
    def Validate (self) -> None :
        self.Valid = bool(Get.MAC_Type(self.Mac) == 'Hex')

    def __str__(self) -> str :
        return self.Dubble if self.Valid else self.Input

    def __bool__(self) -> bool :
        return self.Valid
