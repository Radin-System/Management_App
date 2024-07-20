import re
from Function.decorator import Return_False_On_Exception

MAC_SPECIALS = '.-:,'
SPECIAL_CHARS = '!@#$%^&*()_+"|\\/<>?:;{}[]' + "'"

class Validator:
    def __new__(cls, Input:str):
        Instance = super().__new__(cls)
        Instance.Input = Input
        Instance.Error_Message = 'Something went wrong while validating the input'
        Instance.Check_For_Error()
        return Instance.Input

    def Check_For_Error(self) -> None:
        if not self.Validate():
            raise ValueError(self.Error_Message)

    def Validate(self) -> bool:
        raise NotImplementedError('Subclasses should implement this method.')
    
class Username(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None :
        """
        Usernames can contain letters (a-Z), numbers (0-9), and periods (.). 
        Usernames cannot contain an ampersand (&), equals sign (=), apostrophe ('), plus sign (+), comma (,), brackets (<,>), or more than one period (.)
        The Username can't be smaller than 2 characters .
        Invalid characters are " / \\ [ ] : ; | = , + * ? < > Logon names can contain all other special characters, periods, dashes, and underscores.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided username must be a string: {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z0-9._-]+$' , self.Input) :
            self.Error_Message = f'Provided username only can contain A-Z,a-z,0-9,underscore,dash and dots: {self.Input}'
            return False

        if '..' in self.Input:
            self.Error_Message = f'Provided username can not contain two dots in a row: {self.Input}'
            return False

        if len(self.Input) <= 2:
            self.Error_Message = f'Provided username must contain at least 2 charecters: {self.Input}'
            return False
        
        if len(self.Input) > 64:
            self.Error_Message = f'Provided username can not contain two dots in a row: {self.Input}'
            return False

        if self.Input.isdigit():
            self.Error_Message = f'Provided username can not only contain digits: {self.Input}'
            return False

        return True

class Password(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None:
        """
        complex passwords consist of at least seven characters, 
        including three of the following four character types: uppercase letters, lowercase letters, numeric digits, 
        and non-alphanumeric characters such as & $ * and !.
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = 'Provided Password must be a string'
            return False

        Score = 0
        if any(Char.islower()        for Char in self.Input): Score += 1
        if any(Char.isupper()        for Char in self.Input): Score += 1
        if any(Char.isdigit()        for Char in self.Input): Score += 1
        if any(Char in SPECIAL_CHARS for Char in self.Input): Score += 1

        if len(self.Input) < 7 :
            self.Error_Message = 'Provided password must contain at least 7 charecters'
            return False

        if Score < 3 :
            self.Error_Message = 'Provided password does not meet the complexity rules'
            return False

        return True

class Domain(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
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
            self.Error_Message = f'Provided domain must be a string: {self.Input}'
            return False

        if not '.' in self.Input :
            self.Error_Message = f'Provided domain must contain one or more dots: {self.Input}'
            return False

        if '..' in self.Input :
            self.Error_Message = f'Provided domain can not contain two dots in a row: {self.Input}'
            return False

        if not 4 <= len(self.Input) :
            self.Error_Message = f'Provided domain should have at least 4 charecters: {self.Input}'
            return False

        if not len(self.Input) <= 63 :
            self.Error_Message = f'Provided domain should have maximum of 63 charecters: {self.Input}'
            return False

        Segments = self.Input.split('.')

        if not len(Segments) >= 2 :
            self.Error_Message = f'Provided domain must contain at least two segments (segments are seprated by a dot): {self.Input}'
            return False

        for Segment in Segments :
            if Segment.startswith('-') or Segment.endswith('-'): 
                self.Error_Message = f'Provided domain segment should not start or end with a "-": {self.Input}'
                return False

            if not 2 <= len(Segment): 
                self.Error_Message = f'Provided domains segments must contain at least 2 charecters: {self.Input}'
                return False

            if not len(Segment) <= 63: 
                self.Error_Message = f'Provided domain segments should have maximum of 63 charecters: {self.Input}'
                return False

            if not re.match(r'^[a-zA-Z0-9-]+$', Segment):
                self.Error_Message = f'Provided domain segment only can contain A-Z,a-z,0-9 and "-": {self.Input}'
                return False

        return True

class Email(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None :
        '''
        a valid email contains a username an @ and a domain afterwards.
        Email only contains one @
        '''

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided email must be a string: {self.Input}'
            return False

        if not '@' in self.Input :
            self.Error_Message = f'Provided Email must contain an @: {self.Input}'
            return False
        
        if self.Input.count('@') != 1 :
            self.Error_Message = f'Provided Email should only contain one @: {self.Input}'
            return False
        
        User, Dom = self.Input.split('@',1)

        try: Username(User)
        except Exception as e :
            self.Error_Message = f'Username Error: {self.Input} : {str(e)}'
            return False
        
        try: Domain(Dom)
        except Exception as e :
            self.Error_Message = f'DomainName Error: {self.Input} : {str(e)}'
            return False
        
        return True

class IPv4(Validator):
    def __init__(self, Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> None :
        """
        What makes a valid IPv4 address?
        An IPv4 address has the following format: x . x . x . x where x is called an octet and must be a decimal value between 0 and 255.
        ip can contain / or space and a CIDR or Subnetmask afterwards
        """

        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided IPv4 must be a string: {self.Input}'
            return False


        if '/' in self.Input :
            if self.Input.count('/') != 1 :
                self.Error_Message = f'Provided IPv4 and Mask should only contain one slash: {self.Input}'
                return False

            Ip,Mask = self.Input.split('/',1)

        elif ' ' in self.Input :
            if self.Input.count(' ') != 1 :
                self.Error_Message = f'Provided IPv4 and Mask should only contain one space: {self.Input}'
                return False

            Ip,Mask = self.Input.split(' ',1)

        else :
            Ip = self.Input
            Mask = '255.255.255.255'

        if Ip.count('.') != 3 :
            self.Error_Message = f'Provided IPv4 should contain three dots: {self.Input}'
            return False

        Octets = Ip.split('.',3)

        for Octet in Octets :
            if not Octet.isdigit(): 
                self.Error_Message = f'IP Octets must be digits: {self.Input}'
                return False
            
            if 0 >= int(Octet) >= 255 :
                self.Error_Message = f'IP octets must be betwean or equal to 0 and 255: {self.Input}'
                return False

        if '.' in Mask :
            if Mask.count('.') != 3 :
                self.Error_Message = f'Provided subnet Mask should contain three dots: {self.Input}'
                return False

            Mask_Octets = Mask.split('.',3)
            try: 
                Binary_Mask = ''.join('{:08b}'.format(int(Octet)) for Octet in Mask_Octets)
                if not re.match(r'^1*0*$', Binary_Mask) :
                    self.Error_Message = f'Invalid binary info for Mask: {self.Input}'
                    return False
                
            except Exception as e:
                self.Error_Message = f'Something went wrong while converting subnet mask to binary: {self.Input} : {str(e)}'
                return False
        
        elif Mask.isdigit() :
            if  0 >= int(Mask) >= 32 :
                self.Error_Message = f'CIDR Mask should be betwean or equal to 0 and 32: {self.Input}'
                return False    

        return True

class Mac(Validator):
    def __init__(self,Input:str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool :
        self.Input:str

        if not isinstance(self.Input,str) :
            self.Error_Message = f'Provided mac address must be a string: {self.Input}'
            return False

        Mac = self.Input
        for Item in MAC_SPECIALS: 
            Mac = Mac.replace(Item , '')
        Mac = Mac.upper()

        if not re.match(r'^[A-F0-9]+$', Mac):
            self.Error_Message = f'Provided mac address is not in currect format: {self.Input}'
            return False
        
        return True

class Port(Validator):
    def __init__(self,Input:int) -> None:
        super().__init__(Input)
    
    @Return_False_On_Exception
    def Validate(self) -> bool :
        '''
        port is a number betwen 1 to 65,535
        '''

        self.Input: int

        if not isinstance(self.Input,int) :
            self.Error_Message = f'Provided Port must be a integer: {self.Input}'
            return False

        if self.Input < 1 :
            self.Error_Message = f'Provided Port can not be smaller than 1: {self.Input}'
            return False

        if self.Input > 65535 :
            self.Error_Message = f'Provided Port can not be bigger than 65535: {self.Input}'
            return False

        return True

class English(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only English characters and whitespace.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z\s]+$', self.Input):
            self.Error_Message = f'Provided input can only contain English letters and spaces: {self.Input}'
            return False

        return True

class Persian(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only Persian characters and whitespace.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[\u0600-\u06FF\s]+$', self.Input):
            self.Error_Message = f'Provided input can only contain Persian letters and spaces: {self.Input}'
            return False

        return True

class EnglishSpecial(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only English letters, spaces, and special characters.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[a-zA-Z\s@.0-9\'\"<>\?\!]+$', self.Input):
            self.Error_Message = f'Provided input can only contain English letters, spaces, and special characters: {self.Input}'
            return False

        return True

class PersianSpecial(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input contains only Persian letters, spaces, and special characters.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        if not re.match(r'^[\u0600-\u06FF\s@.0-9\'\"<>\?\!]+$', self.Input):
            self.Error_Message = f'Provided input can only contain Persian letters, spaces, and special characters: {self.Input}'
            return False

        return True
    
class MobileNumber(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)
    
    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input is a Mobile number.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        clean_input = self.Input.replace(" ", "").replace("-", "")

        if not re.match(r'^(\+98|0)?9\d{9}$', clean_input):
            self.Error_Message = f'Provided mobile number is invalid: {self.Input}'
            return False

        return True

class PhoneNumber(Validator):
    def __init__(self, Input: str) -> None:
        super().__init__(Input)

    @Return_False_On_Exception
    def Validate(self) -> bool:
        """
        Validates that the input is a Phone number.
        """

        self.Input:str

        if not isinstance(self.Input, str):
            self.Error_Message = f'Provided input must be a string: {self.Input}'
            return False

        clean_input = self.Input.replace(" ", "").replace("-", "")

        if not re.match(r'^(\+98|0)?\d{5,11}$', clean_input):
            self.Error_Message = f'Provided phone number is invalid: {self.Input}'
            return False

        return True
