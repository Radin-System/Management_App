import uuid
from ._base import Validator
from functions.decorator import Return_False_On_Exception

class Uuid(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input string is a valid UUID.
        A UUID should follow the format of 8-4-4-4-12 hexadecimal digits (e.g., 123e4567-e89b-12d3-a456-426614174000).
        """
        
        self.Input: str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided UUID must be a string: {self.Input}'
            return False

        try:
            # Attempt to create a UUID object to check if the input is a valid UUID
            Object = uuid.UUID(self.Input)
        except ValueError:
            self.Error_Message = f'Provided string is not a valid UUID: {self.Input}'
            return False

        if str(Object) != self.Input:
            self.Error_Message = f'Provided UUID does not match standard format: {self.Input}'
            return False

        return True