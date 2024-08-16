import re
from .base import Validator
from functions.decorator import Return_False_On_Exception

SPECIAL_CHARS = '!@#$%^&*()_+"|\\/<>?:;{}[]' + "'"

class Password(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None:
        """
        complex passwords consist of at least seven characters, 
        including three of the following four character types: uppercase letters, lowercase letters, numeric digits, 
        and non-alphanumeric characters such as & $ * and !.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = 'Provided Password must be a string'
            return False

        if not re.match(r'^[a-zA-Z\s@.0-9\'\"<>\?\!]+$', self.Input):
            self.Error_Message = f'Provided Password can only contain English letters, spaces, and special characters'
            return False

        Score = 0
        if any(Char.islower()        for Char in self.Input): Score += 1
        if any(Char.isupper()        for Char in self.Input): Score += 1
        if any(Char.isdigit()        for Char in self.Input): Score += 1
        if any(Char in SPECIAL_CHARS for Char in self.Input): Score += 1

        if len(self.Input) < 7:
            self.Error_Message = 'Provided password must contain at least 7 charecters'
            return False

        if Score < 3:
            self.Error_Message = 'Provided password does not meet the complexity rules'
            return False

        return True