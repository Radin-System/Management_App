import re
from . import Validator
from Function.decorator import Return_False_On_Exception

class Username(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None :
        """
        Usernames can contain letters (a-Z), numbers (0-9), and periods (.). 
        Usernames cannot contain an ampersand (&), equals sign (=), apostrophe ('), plus sign (+), comma (,), brackets (<,>), or more than one period (.)
        The Username can't be smaller than 2 characters .
        Invalid characters are " / \\ [ ] : ; | = , + * ? < > Logon names can contain all other special characters, periods, dashes, and underscores.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided username must be a string : {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z0-9._-]+$' , self.Input) :
            self.Error_Message = f'Provided username only can contain A-Z,a-z,0-9,underscore,dash and dots : {self.Input}'
            return False

        if '..' in self.Input:
            self.Error_Message = f'Provided username can not contain two dots in a row : {self.Input}'
            return False

        if len(self.Input) <= 2:
            self.Error_Message = f'Provided username must contain at least 2 charecters : {self.Input}'
            return False
        
        if len(self.Input) > 64:
            self.Error_Message = f'Provided username can not contain two dots in a row : {self.Input}'
            return False

        if self.Input.isdigit():
            self.Error_Message = f'Provided username can not only contain digits : {self.Input}'
            return False

        return True