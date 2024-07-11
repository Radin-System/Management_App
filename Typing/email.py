from Class import Validator
from Class import Decorator
from . import Username,Domain

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

        if not '@' in self.Input :
            self.Error_Message = 'Provided Email must contain an @'
            return False
        
        if self.Input.count('@') != 1 :
            self.Error_Message = 'Provided Email should only contain one @'
            return False
        
        User, Dom = self.Input.split('@',1)

        try : Username(User)
        except Exception as e :
            self.Error_Message = f'Username Error <{User}> : {str(e)}'
            return False
        
        try : Domain(Dom)
        except Exception as e :
            self.Error_Message = f'DomainName Error <{Dom}> : {str(e)}'
            return False
        
        return True
