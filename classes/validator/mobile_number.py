import re
from ._base import Validator
from functions.decorator import Return_False_On_Exception

class MobileNumber(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)
    
    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input is a Mobile number.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        clean_input = self.Input.replace(" ", "").replace("-", "")

        if not re.match(r'^(\+98|0)?9\d{9}$', clean_input):
            self.Error_Message = f'Provided mobile number is invalid: {self.Input}'
            return False

        return True
