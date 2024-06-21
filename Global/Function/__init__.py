import os , re , hashlib
from Global.Constant     import ENCODE , MAC_PATTERN_MAP , CIDR_MAP , MASK_MAP , PORT_MAP , PORT_TYPE_MAP , MAX_HOST_RANGE_SUBNET
from cryptography.fernet import Fernet

def Pass () : pass

class Validate :

    @staticmethod
    def Mac (Mac) -> bool :
        for Pattern in MAC_PATTERN_MAP.values() :
            if re.match(Pattern , Mac) : return True
        return False
    
    @staticmethod
    def Vlan (Number : int , Name : str) -> bool : # Not Compleated
        if ' ' not in Name :
            return 0 < Number < 1023 
        return False

    @staticmethod
    def IPv4 (IP : str) -> bool :
        """
        What makes a valid IPv4 address?
        An IPv4 address has the following format: x . x . x . x where x is called an octet and must be a decimal value between 0 and 255.
        """
        Octets = IP.split('.')
        if len(Octets) != 4 : return False
        for Octet in Octets :
            if not Octet.isdigit() : return False
            Octet_Value = int(Octet)
            if 0 >= Octet_Value >= 255 : return False
        return True

    @staticmethod
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
    def Port (Portnumber : int) -> bool :
        if isinstance(Portnumber,int) :
            return 1 < Portnumber < 65535
        return False
    
    @staticmethod
    def Protocol (Protocol : str) -> bool :
        Valid = list(PORT_MAP.keys())
        Valid.extend(list(PORT_TYPE_MAP.keys()))
        return bool(Protocol.upper() in Valid)
        
    
    @staticmethod
    def DefaultProtocol (Portnumber : int , Protocol : str) -> bool :
        if Validate.Protocol(Protocol) and Validate.Port(Portnumber) :
            Default = PORT_MAP.get(Protocol.upper(),{})
            return bool( Protocol.upper() not in PORT_TYPE_MAP.keys()
                and Default 
                and Default.get('Default_Number',0) == Portnumber )
        return False

    @staticmethod
    def WellKhown (Portnumber : int) -> bool :
        if Validate.Port(Portnumber) :
            return bool(1 <= Portnumber <= 1023)
        return False
    
    @staticmethod
    def Addr (Addr : str) -> bool :
        if ':' in Addr :
            IP , Protocol = Addr.split(':',1)
            return Validate.IPv4(IP) and Validate.Port(Protocol)
        return False

    @staticmethod
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
    def MD5(Password : str) -> bool :
        MD5_Pattern = re.compile(r'^[0-9a-fA-F]{32}$')
        return bool(MD5_Pattern.match(Password))

    @staticmethod
    def Crypted(Passwprd) -> bool :
        pass

    @staticmethod
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

    def Phone(Phone_Number):
        # Regular expression to match a phone number starting with '+'
        Pattern = r'^(\+(?:[0-9] ?){6,14}[0-9]|0[0-9]{2} ?(?:[0-9] ?){8,10})$'
        return bool(re.match(Pattern, Phone_Number))

class Get :
    
    @staticmethod
    def MAC_Type(Mac) -> str :
        for Type , Pattern in MAC_PATTERN_MAP.items() :
            if re.match(Pattern , Mac) : return Type
        return ''

    @staticmethod
    def Octets(String : str) -> list :
        Octets = String.split('.')
        return Octets if len(Octets) == 4 else []
        

    @staticmethod
    def Position(IP : str , Subnet : str) -> int : # Not Compleated
        pass

    @staticmethod
    def IP_Class(IP : str) -> str : # Not Compleated
        """
        Class A: Addresses in the range 0.0.0.0 to 127.255.255.255. The first bit is always 0.
        Class B: Addresses in the range 128.0.0.0 to 191.255.255.255. The first two bits are always 10.
        Class C: Addresses in the range 192.0.0.0 to 223.255.255.255. The first three bits are always 110.
        Class D: Reserved for multicast (224.0.0.0 to 239.255.255.255)
        Class E: Reserved for experimental (240.0.0.0 to 255.255.255.255)
        """
        pass

    @staticmethod
    def IP_Type(IP : str) -> str : # Not Compleated
        """
        Public IP address ranges:
        Class A: 0.0.0.0 to 127.255.255.255 (First bit: 0)
        Class B: 128.0.0.0 to 191.255.255.255 (First two bits: 10)
        Class C: 192.0.0.0 to 223.255.255.255 (First three bits: 110)
        Class D: Reserved for multicast (224.0.0.0 to 239.255.255.255)
        Class E: Reserved for experimental (240.0.0.0 to 255.255.255.255)
        Private IP address ranges:
        Class A: 10.0.0.0 to 10.255.255.255 (10.0.0.0/8)
        Class B: 172.16.0.0 to 172.31.255.255 (172.16.0.0/12)
        Class C: 192.168.0.0 to 192.168.255.255 (192.168.0.0/16)
        """

    @staticmethod
    def NetID(IP : str, Subnet : str) -> str :
        """
        In IPv4 addresses, the Net ID is determined by the network's subnet mask. 
        The subnet mask is a 32-bit number that specifies which portion of an IP address is the network portion and which portion is the host portion.
        """
        if Validate.IPv4(IP) and (Validate.Mask(Subnet) or Validate.CIDR(Subnet)) :
            if Validate.CIDR(Subnet) : Subnet = Convert.CIDRToMask(Subnet)
            IP_Octets     = list(map(int , Get.Octets(IP    )))
            Mask_Octets   = list(map(int , Get.Octets(Subnet)))
            Net_ID_Octets = [str(IP_Octets[i] & Mask_Octets[i]) for i in range(4)]
            return '.'.join(Net_ID_Octets)
        else : return ''

    @staticmethod
    def Broadcast(IP: str, Subnet : str) -> str :
        """
        The "broadcast IP" refers to a specific IP address within a network that is used for broadcasting messages to all devices on that network.
        In IPv4 networking, the broadcast IP address is the highest address in the network range, with all host bits set to 1. 
        This means that all devices within the network will receive broadcast messages sent to this address.
        For example, in a network with the IP address range 192.168.1.0/24 (where the subnet mask is 255.255.255.0),
        the broadcast IP address would be 192.168.1.255. 
        Any message sent to this address would be received by all devices within the network segment 192.168.1.0 to 192.168.1.255.
        """
        if Validate.IPv4(IP) and (Validate.Mask(Subnet) or Validate.CIDR(Subnet)) :
            if Validate.CIDR(Subnet) : Subnet = Convert.CIDRToMask(Subnet)
            IP_Octets = list(map(int , Get.Octets(IP)))
            Mask_Octets = list(map(int , Get.Octets(Subnet)))
            Broadcast_Octets = [(IP_Octets[i] | ~Mask_Octets[i]) & 255 for i in range(4)]
            return '.'.join(map(str, Broadcast_Octets))
        else : return '' 

    @staticmethod
    def IPs(IP : str , Subnet : str) -> list :
        """
        The number of possible hosts refers to the maximum number of devices or hosts that can be connected to a network segment. 
        It is determined by the number of host bits available in the subnet mask.
        In IPv4 networking, the number of possible hosts can be calculated using the formula:
        Possible Hosts = 2^(Number of Host Bits) - 2
        """
        if Validate.IPv4(IP) and (Validate.Mask(Subnet) or Validate.CIDR(Subnet)) :
            def Increment (IP_Address) :
                IP_Octets = Get.Octets(IP_Address)[::-1]
                IP_Octets = [int(Octet) for Octet in IP_Octets]
                Carryover = 0
                Result = []
                for i in range(len(IP_Octets)):
                    Digit_Sum = IP_Octets[i] + (1,0,0,0)[i] + Carryover
                    Result.append(Digit_Sum % 256)
                    Carryover = Digit_Sum // 256
                if Carryover > 0 : Result.append(Carryover)
                return ".".join(map(str, Result[::-1]))
            
            Max_CIDR = MAX_HOST_RANGE_SUBNET if Validate.CIDR(MAX_HOST_RANGE_SUBNET) else Convert.MaskToCIDR(MAX_HOST_RANGE_SUBNET)
            if Validate.Mask(Subnet) : Subnet = Convert.MaskToCIDR(Subnet)
            if not int(Subnet[1:]) >= int(Max_CIDR[1:]) : raise ValueError(f'The subnet provided is too large')
            First_IP   = Get.NetID(IP,Subnet)
            Last_IP    = Get.Broadcast(IP,Subnet)
            Current_IP = First_IP
            Hosts = [Current_IP]
            while Current_IP != Last_IP :
                Current_IP = Increment(Current_IP)
                Hosts.append(Current_IP)
            return Hosts
        return []

    @staticmethod
    def Port_Type (Protocol : str) -> list :
        if Validate.Protocol(Protocol) : 
            if Protocol.upper() in PORT_TYPE_MAP.keys() : return [Protocol]
            else : return PORT_MAP.get(Protocol.upper(),{}).get('Type',[])
        return []
    
    @staticmethod
    def Port_Number (Name : str) -> int :
        return int(PORT_MAP.get(str(Name),{}).get('Default_Number',0))

    @staticmethod
    def DN(Domain:str) -> str:
        if Validate.Domain(Domain) :
            Components = Domain.split('.')
            Search_Base = ','.join(f'dc={Component}' for Component in Components)
        return Search_Base

class Convert :

    @staticmethod
    def MaskToCIDR(Mask : str) -> str :
        if Validate.Mask(Mask) :
           return CIDR_MAP.get(Mask , '')
        return ''

    @staticmethod
    def CIDRToMask(CIDR : str) -> str :
        if Validate.CIDR(CIDR) :
            return MASK_MAP.get(CIDR , '')
        return ''

class Crypto :
    
    @staticmethod
    def MD5 (Raw : str) -> str :
        MD5 = hashlib.md5()
        MD5.update(Raw.encode())
        return MD5.hexdigest()

    @staticmethod
    def Generate() -> bytes:
        return Fernet.generate_key()
    
    @staticmethod
    def Encrypt(Phrase : str) -> bytes :
        Key = os.environ.get('CRYPTO_KEY' , None)
        if not Key : raise ValueError("CRYPTO_KEY environment variable not set")
        frenet = Fernet(Key.encode(ENCODE))
        return frenet.encrypt(Phrase.encode(ENCODE))
    
    @staticmethod
    def Decrypt(Token : bytes) -> str :
        Key = os.environ.get('CRYPTO_KEY' , None)
        if not Key : raise ValueError("CRYPTO_KEY environment variable not set")
        frenet = Fernet(Key.encode(ENCODE))
        return frenet.decrypt(Token).decode(ENCODE)
