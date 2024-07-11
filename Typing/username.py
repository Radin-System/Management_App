import re
from Class import Validator
from Class import Decorator

class Username(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Decorator.Return_False_On_Exception
    def Validate(self) -> None :
        """
        Usernames can contain letters (a-Z), numbers (0-9), and periods (.). 
        Usernames cannot contain an ampersand (&), equals sign (=), apostrophe ('), plus sign (+), comma (,), brackets (<,>), or more than one period (.)
        The Username can't be smaller than 2 characters .
        Invalid characters are " / \\ [ ] : ; | = , + * ? < > Logon names can contain all other special characters, periods, dashes, and underscores.
        """

        self.Input:str

        if not re.match(r'^[a-zA-Z0-9._-]+$' , self.Input) :
            self.Error_Message = 'Provided username only can contain A-Z,a-z,0-9,underscore,dash and dots'
            return False

        if '..' in self.Input:
            self.Error_Message = 'Provided username can not contain two dots in a row'
            return False

        if len(self.Input) <= 2:
            self.Error_Message = 'Provided username must contain at least 2 charecters'
            return False
        
        if len(self.Input) > 64:
            self.Error_Message = 'Provided username can not contain two dots in a row'
            return False

        if self.Input.isdigit():
            self.Error_Message = 'Provided username can not only contain digits'
            return False

        return True