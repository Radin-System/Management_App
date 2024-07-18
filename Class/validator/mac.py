import re
from . import Validator
from Class.decorator import Decorator

MAC_SPECIALS = '.-:,'

class Mac(Validator):
    def __init__(self,Input:str) -> None:
        super().__init__(Input)

    @Decorator.Return_False_On_Exception
    def Validate(self) -> bool :
        self.Input : str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided mac address must be a string : {self.Input}'
            return False

        Mac = self.Input
        for Item in MAC_SPECIALS : 
            Mac = Mac.replace(Item , '')
        Mac = Mac.upper()

        if not re.match(r'^[A-F0-9]+$', Mac):
            self.Error_Message = f'Provided mac address is not in currect format : {self.Input}'
            return False
        
        return True
