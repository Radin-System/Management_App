
class Vlan : # Not Compleated
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        self.Number , self.Name = self.Input.split('-',1)
        self.Number = int(self.Name.upper().replace('VLAN',''))
        self.Validate()

    def Validate(self) -> None :
        self.Valid = Validate.Vlan(self.Number , self.Name)

    def __str__(self) -> str :
        return f'VLAN{self.Number}-{self.Name}'

    def __bool__(self) -> bool :
        return self.Valid
