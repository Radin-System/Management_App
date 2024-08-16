import re
from ._base import Validator
from functions.decorator import Return_False_On_Exception

class Hostname(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Valid hostname onlu contains 16 chars, a-Z , 0-9 and dashes
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if len(self.Input) < 2:
            self.Error_Message = f'Provided hostname is too short: {self.Input}'
            return False

        if len(self.Input) > 16:
            self.Error_Message = f'Provided hostname is too long: {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z0-9-]{1,16}$', self.Input):
            self.Error_Message = f'Provided hostname can only contain letters, digits, and hyphens: {self.Input}'
            return False

        return True