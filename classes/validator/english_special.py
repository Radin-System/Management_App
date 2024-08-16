import re
from .base import Validator
from functions.decorator import Return_False_On_Exception

class EnglishSpecial(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only English letters, spaces, and special characters.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z\s@.0-9\'\"<>\?\!.-]+$', self.Input):
            self.Error_Message = f'Provided input can only contain English letters, spaces, and special characters: {self.Input}'
            return False

        return True
