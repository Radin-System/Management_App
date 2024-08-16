from .base import Validator
from functions.decorator import Return_False_On_Exception
from .fqdn import FQDN
from .ipv4 import IPv4

class IPv4OrFQDN(Validator):
    def __init__(self,Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool :
        """
        Checks if input is Ip address or FQDN.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided Input must be a string: {self.Input}'
            return False

        try: FQDN(self.Input)
        except ValueError:
            try: IPv4(self.Input)
            except ValueError as e:
                self.Error_Message = f'Provided input is nether a IPv4 or a FQDN: {self.Input}'
                return False
        
        return True