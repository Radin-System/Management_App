class Domain :
    def __init__(self , DomainName : str ) -> None :
        self.Domain = DomainName.strip()
        self.Validate()
        if self.Valid :
            self.DN            = Get.DN(self.Domain)
            self.LDAP_Endpoint = f'ldap://{self.Domain}'

    def Validate(self) -> None :
        self.Valid = Validate.Domain(self.Domain)

    def __str__ (self) -> str :
        return f'{self.Domain}'
       
    def __bool__ (self) -> bool :
        return self.Valid
