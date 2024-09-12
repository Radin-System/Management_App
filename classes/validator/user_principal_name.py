from ._base import Validator
from .username import Username
from .domain import Domain
from functions.decorator import Return_False_On_Exception

class UserPrincipalName(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None :
        """
        User Principal has two parts : Username@DomainName

        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided username must be a string: {self.Input}'
            return False

        if not '@' in self.Input:
            self.Error_Message = f'Username must contain at least one @: {self.Input}'
            return False
        
        User, DomainName = self.Input.split('@',1)

        try:
            Username(User)
        except ValueError as e:
            self.Error_Message = f'Username Error: {e}'
            return False

        try:
            Domain(DomainName)
        except ValueError as e:
            self.Error_Message = f'Domain Error: {e}'
            return False

        return True