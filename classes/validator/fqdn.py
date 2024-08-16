from .base import Validator
from .hostname import Hostname
from .domain import Domain
from functions.decorator import Return_False_On_Exception

class FQDN(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool :
        """
        FQDN has two parts : Hostname.DomainName
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided email must be a string: {self.Input}'
            return False
        
        if not '.' in self.Input :
            self.Error_Message = f'Provided FQDN must contain one or more dots: {self.Input}'
            return False

        Host, Dom = self.Input.split('.',1)

        try: Hostname(Host)
        except Exception as e :
            self.Error_Message = f'Hostname Error: {self.Input} : {str(e)}'
            return False
        
        try: Domain(Dom)
        except Exception as e :
            self.Error_Message = f'DomainName Error: {self.Input} : {str(e)}'
            return False
        
        return True