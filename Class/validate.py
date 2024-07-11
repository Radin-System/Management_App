import re
from constants import MAC_PATTERN_MAP, PORT_MAP, PORT_TYPE_MAP
from . import Decorator
from . import Get

class Validate :

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Mac (Mac) -> bool :
        for Pattern in MAC_PATTERN_MAP.values() :
            if re.match(Pattern , Mac) : return True
        return False

    @staticmethod
    @Decorator.Return_False_On_Exception
    def IPv4 (IP : str) -> bool :
        """
        What makes a valid IPv4 address?
        An IPv4 address has the following format: x . x . x . x where x is called an octet and must be a decimal value between 0 and 255.
        """
        Octets = Get.Octets(IP)
        if not Octets : return False
        for Octet in Octets : 
            if not Octet.isdigit() and 0 >= int(Octet) >= 255 : return False
        return True

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Mask(Mask : str) -> bool :
        """
        What is Valid Subnet Mask ?
        A Subnet Mask has the following format: x . x . x . x where x is called an octet and must be a decimal value from the following list : [ 0 , 128 , 192 , 224 , 240 , 248 , 252 , 254 , 255]
        the subnet grows from right to left and must fill the first octet with 255 then it can change other octets from 0
        """
        Octets = Get.Octets(Mask)
        if Octets :
            Binary_Mask = ''.join('{:08b}'.format(int(Octet)) for Octet in Octets)
            return bool(re.match(r'^1*0*$', Binary_Mask))
        return False

    @staticmethod
    @Decorator.Return_False_On_Exception
    def CIDR(CIDR : str) -> bool :
        """
        What is Valid CIDR ?
        a valid CIDR contains a '/' as the first charecter and has a number afterwards .
        the number is between 0 and 32 .
        """
        if not re.match(r'^/\d{1,2}$', CIDR) : return False
        Subnet_Bits = int(CIDR[1:])
        return 0 <= Subnet_Bits <= 32
