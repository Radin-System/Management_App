from . import Validator
from Function.decorator import Return_False_On_Exception

class Port(Validator):
    def __init__(self,Input:int) -> None:
        super().__init__(Input)
    
    @Return_False_On_Exception
    def Validate(self) -> bool :
        '''
        port is a number betwen 1 to 65,535
        '''

        self.Input : int

        if not isinstance(self.Input,int) :
            self.Error_Message = f'Provided Port must be a integer : {self.Input}'
            return False

        if self.Input < 1 :
            self.Error_Message = f'Provided Port can not be smaller than 1 : {self.Input}'
            return False

        if self.Input > 65535 :
            self.Error_Message = f'Provided Port can not be bigger than 65535 : {self.Input}'
            return False

        return True