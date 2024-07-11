class Get :

    @staticmethod
    def MAC_Type(Mac) -> str :
        for Type , Pattern in MAC_PATTERN_MAP.items() :
            if re.match(Pattern , Mac) : return Type
        return ''

    @staticmethod
    def Octets(String : str) -> list[str] :
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

            if Validate.Mask(Subnet) : Subnet = Convert.MaskToCIDR(Subnet)
            if not int(Subnet[1:]) >= 16 : raise ValueError(f'The subnet provided is too large')
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
