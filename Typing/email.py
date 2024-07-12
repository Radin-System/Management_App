from Class.validator import Validator
from Class.decorator import Decorator
from .domain import Domain
from .username import Username

class Email(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Decorator.Return_False_On_Exception
    def Validate(self) -> None :
        '''
        a valid email contains a username an @ and a domain afterwards.
        Email only contains one @
        '''

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided email must be a string : {self.Input}'
            return False

        if not '@' in self.Input :
            self.Error_Message = f'Provided Email must contain an @ : {self.Input}'
            return False
        
        if self.Input.count('@') != 1 :
            self.Error_Message = f'Provided Email should only contain one @ : {self.Input}'
            return False
        
        User, Dom = self.Input.split('@',1)

        try : Username(User)
        except Exception as e :
            self.Error_Message = f'Username Error : {self.Input} : {str(e)}'
            return False
        
        try : Domain(Dom)
        except Exception as e :
            self.Error_Message = f'DomainName Error : {self.Input} : {str(e)}'
            return False
        
        return True
