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
    def Vlan (Number : int , Name : str) -> bool : # Not Compleated
        return ' ' not in Name and 0 < Number < 1023

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

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Port (Portnumber : int) -> bool :
        if isinstance(Portnumber,int) :
            return 1 < Portnumber < 65535
        return False
    
    @staticmethod
    @Decorator.Return_False_On_Exception
    def Protocol (Protocol : str) -> bool :
        Valid = list(PORT_MAP.keys())
        Valid.extend(list(PORT_TYPE_MAP.keys()))
        return bool(Protocol.upper() in Valid)
        
    
    @staticmethod
    @Decorator.Return_False_On_Exception
    def DefaultProtocol (Portnumber : int , Protocol : str) -> bool :
        if Validate.Protocol(Protocol) and Validate.Port(Portnumber) :
            Default = PORT_MAP.get(Protocol.upper(),{})
            return bool( Protocol.upper() not in PORT_TYPE_MAP.keys()
                and Default 
                and Default.get('Default_Number',0) == Portnumber )
        return False

    @staticmethod
    @Decorator.Return_False_On_Exception
    def WellKhown (Portnumber : int) -> bool :
        if Validate.Port(Portnumber) :
            return bool(1 <= Portnumber <= 1023)
        return False
    
    @staticmethod
    @Decorator.Return_False_On_Exception
    def Addr (Addr : str) -> bool :
        if ':' in Addr :
            IP , Protocol = Addr.split(':',1)
            return Validate.IPv4(IP) and Validate.Port(Protocol)
        return False

    @staticmethod
    @Decorator.Return_False_On_Exception
    def User (Username) -> bool :
        """
        What is the valid username ?
        Usernames can contain letters (a-z), numbers (0-9), and periods (.). 
        Usernames cannot contain an ampersand (&), equals sign (=), underscore (_), apostrophe ('), dash (-), plus sign (+), comma (,), brackets (<,>), or more than one period (.)
        Logon names can't contain certain characters.
        The Username can't be smaller than 2 characters .
        Invalid characters are " / \\ [ ] : ; | = , + * ? < > Logon names can contain all other special characters, including spaces, periods, dashes, and underscores.
        But it's generally not a good idea to use spaces in account names.
        """
        return bool( re.match(r'^[a-zA-Z0-9._ -]+$' , Username) 
            and ".." not in Username 
            and 2 <= len(Username) <= 64
            and not '  ' in Username
            and not Username.isdigit() )

    @staticmethod
    @Decorator.Return_False_On_Exception
    def MD5(Password : str) -> bool :
        MD5_Pattern = re.compile(r'^[0-9a-fA-F]{32}$')
        return bool(MD5_Pattern.match(Password))

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Crypted(Passwprd) -> bool :
        pass

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Domain(Domain) -> bool : # Has Problems
        """
        How do I create a valid domain ?
        A domain name consists of minimum four and maximum 63 characters.
        At least one period (.) is required
        Each segment consist of at least 2 charecters.
        All letters from a to z, all numbers from 0 to 9 and a hyphen (-) are possible.
        """
        Segments = Domain.split('.')
        if not (4 <= len(Domain) <= 63 and len(Segments) >= 2) : return False
        for Segment in Segments :
            if ( not 2 <= len(Segment) <= 63 
            and Segment.startswith('-') 
            and Segment.endswith('-')
            and not re.match(r'^[a-zA-Z0-9-]+$', Segment) ) : return False
        return True
    
    @staticmethod
    @Decorator.Return_False_On_Exception
    def Email (Email_Address) -> bool :
        """
        Email addresses are commonly used for electronic mail communication and are structured in this way to uniquely identify recipients and their email providers. 
        They follow the format local-part@domain, where the local part can contain various characters including :
            letters, digits, and certain special characters like dots (.), hyphens (-), and underscores (_). 
        The domain part typically consists of the domain name of the email provider followed by a top-level domain (TLD) such as .com, .org, .net, .edu, .gov, 
        or a country code top-level domain (ccTLD) like .uk, .us, .fr, .jp, etc.
        """
        if '@' in Email_Address :
            Username , DomainName = Email_Address.split('@',1)
            if Validate.User(Username) and Validate.Domain(DomainName) and ' ' not in Username : return True
        return False

    @staticmethod
    @Decorator.Return_False_On_Exception
    def Phone(Phone_Number):
        # Regular expression to match a phone number starting with '+'
        Pattern = r'^(\+(?:[0-9] ?){6,14}[0-9]|0[0-9]{2} ?(?:[0-9] ?){8,10})$'
        return bool(re.match(Pattern, Phone_Number))
