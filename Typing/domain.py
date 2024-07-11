import re
from Class import Validator,Decorator

class Domain(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Decorator.Return_False_On_Exception
    def Validate(self) -> bool :
        """
        How do I create a valid domain ?
        A domain name consists of minimum four and maximum 63 characters.
        At least one period (.) is required
        Each segment consist of at least 2 charecters.
        All letters from a to z, all numbers from 0 to 9 and a hyphen (-) are possible.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided domain must be a string : {self.Input}'
            return False

        if not '.' in self.Input :
            self.Error_Message = f'Provided domain must contain one or more dots : {self.Input}'
            return False

        if '..' in self.Input :
            self.Error_Message = f'Provided domain can not contain two dots in a row : {self.Input}'
            return False

        if not 4 <= len(self.Input) :
            self.Error_Message = f'Provided domain should have at least 4 charecters : {self.Input}'
            return False

        if not len(self.Input) <= 63 :
            self.Error_Message = f'Provided domain should have maximum of 63 charecters : {self.Input}'
            return False

        Segments = self.Input.split('.')

        if not len(Segments) >= 2 :
            self.Error_Message = f'Provided domain must contain at least two segments (segments are seprated by a dot) : {self.Input}'
            return False

        for Segment in Segments :
            if Segment.startswith('-') or Segment.endswith('-'): 
                self.Error_Message = f'Provided domain segment should not start or end with a "-" : {self.Input}'
                return False

            if not 2 <= len(Segment): 
                self.Error_Message = f'Provided domains segments must contain at least 2 charecters : {self.Input}'
                return False

            if not len(Segment) <= 63: 
                self.Error_Message = f'Provided domain segments should have maximum of 63 charecters : {self.Input}'
                return False

            if not re.match(r'^[a-zA-Z0-9-]+$', Segment):
                self.Error_Message = f'Provided domain segment only can contain A-Z,a-z,0-9 and "-" : {self.Input}'
                return False

        return True