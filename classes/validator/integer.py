from ._base import Validator
from functions.decorator import Return_False_On_Exception

class Integer(Validator):
    def __init__(self, Input: int) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Valid hostname onlu contains 16 chars, a-Z , 0-9 and dashes
        """

        self.Input:int

        if not isinstance(self.Input, int):
            self.Error_Message = f'Provided input must be an integer: {self.Input}'
            return False

        return True