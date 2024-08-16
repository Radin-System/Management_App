import re
from .base import Validator
from functions.decorator import Return_False_On_Exception

class Persian(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only Persian characters and whitespace.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[\u0600-\u06FF\s]+$', self.Input):
            self.Error_Message = f'Provided input can only contain Persian letters and spaces: {self.Input}'
            return False

        return True