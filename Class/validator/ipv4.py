import re
from . import Validator
from Class.decorator import Decorator

class IPv4(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Decorator.Return_False_On_Exception
    def Validate(self) -> None :
        """
        What makes a valid IPv4 address?
        An IPv4 address has the following format: x . x . x . x where x is called an octet and must be a decimal value between 0 and 255.
        ip can contain / or space and a CIDR or Subnetmask afterwards
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided IPv4 must be a string : {self.Input}'
            return False


        if '/' in self.Input :
            if self.Input.count('/') != 1 :
                self.Error_Message = f'Provided IPv4 and Mask should only contain one slash : {self.Input}'
                return False

            IP,Mask = self.Input.split('/',1)

        elif ' ' in self.Input :
            if self.Input.count(' ') != 1 :
                self.Error_Message = f'Provided IPv4 and Mask should only contain one space : {self.Input}'
                return False

            IP,Mask = self.Input.split(' ',1)

        else :
            IP = self.Input
            Mask = '255.255.255.255'

        if IP.count('.') != 3 :
            self.Error_Message = f'Provided IPv4 should contain three dots : {self.Input}'
            return False

        Octets = IP.split('.',3)

        for Octet in Octets :
            if not Octet.isdigit(): 
                self.Error_Message = f'IP Octets must be digits : {self.Input}'
                return False
            
            if 0 >= int(Octet) >= 255 :
                self.Error_Message = f'IP octets must be betwean or equal to 0 and 255  : {self.Input}'
                return False

        if '.' in Mask :
            if Mask.count('.') != 3 :
                self.Error_Message = f'Provided subnet Mask should contain three dots : {self.Input}'
                return False

            Mask_Octets = Mask.split('.',3)
            try : 
                Binary_Mask = ''.join('{:08b}'.format(int(Octet)) for Octet in Mask_Octets)
                if not re.match(r'^1*0*$', Binary_Mask) :
                    self.Error_Message = f'Invalid binary info for Mask : {self.Input}'
                    return False
                
            except Exception as e:
                self.Error_Message = f'Something went wrong while converting subnet mask to binary : {self.Input} : {str(e)}'
                return False
        
        elif Mask.isdigit() :
            if  0 >= int(Mask) >= 32 :
                self.Error_Message = f'CIDR Mask should be betwean or equal to 0 and 32 : {self.Input}'
                return False    

        return True
