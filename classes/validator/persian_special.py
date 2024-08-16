import re
from .base import Validator
from functions.decorator import Return_False_On_Exception

class PersianSpecial(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only Persian letters, spaces, and special characters.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[\u0600-\u06FF\s@.0-9\'\"<>\?\!.-]+$', self.Input):
            self.Error_Message = f'Provided input can only contain Persian letters, spaces, and special characters: {self.Input}'
            return False

        return True

