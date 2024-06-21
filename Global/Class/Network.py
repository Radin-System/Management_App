import os , ssl , ldap3
from Global.Constant     import ENCODE , SPECIAL_CHARS , RESERVED_USERS , RESERVED_EMAILS , LDAPUSER_USE_SSL , LDAPUSER_VALIDATE_SSL
from Global.Function     import Validate , Get , Convert , Crypto

class MAC :
    def __init__(self , Input : str) -> None :
        
        Strip = '.-:,'
        self.Input = Input.strip()
        
        for Item in Strip : self.Mac = self.Input.replace(Item , '')
        
        self.Validate()

        if self.Valid :
            self.Hex    = self.Mac.upper()
            self.Dotted = '.'.join([self.Mac.lower()[i:i+4] for i in range(0,12,4)])
            self.Dubble = ':'.join([self.Mac.upper()[i:i+2] for i in range(0,12,2)])
        
    def Validate (self) -> None :
        self.Valid = bool(Get.MAC_Type(self.Mac) == 'Hex')

    def __str__(self) -> str :
        return self.Dubble if self.Valid else self.Input

    def __bool__(self) -> bool :
        return self.Valid

class Vlan : # Not Compleated
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        self.Number , self.Name = self.Input.split('-',1)
        self.Number = int(self.Name.upper().replace('VLAN',''))
        self.Validate()

    def Validate(self) -> None :
        self.Valid = Validate.Vlan(self.Number , self.Name)

    def __str__(self) -> str :
        return f'VLAN{self.Number}-{self.Name}'

    def __bool__(self) -> bool :
        return self.Valid

class IPv4 : # Not Compleated
    def __init__(self , Input : str) -> None : 
        self.Input = Input.strip()

        if '/' in self.Input :
            self.IPv4 , self.Subnet = self.Input.split('/',1)
        else :
            self.IPv4 = self.Input
            self.Subnet = ''

        self.Validate()

        if self.Valid :
            if self.Subnet :
                self.CIDR = '/'+self.Subnet if Validate.CIDR('/'+self.Subnet) else Convert.MaskToCIDR(self.Subnet)
                self.Mask =  self.Subnet    if Validate.Mask(self.Subnet)     else Convert.CIDRToMask('/'+self.Subnet)
            else :
                self.CIDR = '/32'
                self.Mask = '255.255.255.255'
            self.Position  = Get.Position(self.IPv4,self.CIDR)
            self.Class     = Get.IP_Class(self.IPv4)
            self.Type      = Get.IP_Type(self.IPv4)
            self.NetID     = Get.NetID(self.IPv4,self.CIDR)
            self.Broadcast = Get.Broadcast(self.IPv4,self.CIDR)
            self.IPs       = Get.IPs(self.IPv4,self.CIDR)
            self.Hosts     = self.IPs[1:-1]
            self.Host      = True if self.CIDR == '/32' or ( self.NetID != self.IPv4 and self.Broadcast != self.IPv4 ) else False

    def Validate(self) -> None :
        if Validate.IPv4(self.IPv4):
            if self.Subnet and ( Validate.Mask(self.Subnet) or Validate.CIDR('/'+self.Subnet) ) : self.Valid = True
            elif not self.Subnet : self.Valid = True
            else : self.Valid = False
        else : self.Valid = False
    
    def __str__ (self) -> str :
        return f'{self.IPv4}/{self.CIDR}' if self.Valid else self.Input
    
    def __bool__ (self) -> bool :
        return self.Valid
    
class IPv6 : # Not Compleated
    def __init__(self , IP : str) -> None :
        pass

class Port :
    def __init__(self , Input : str) -> None :
        """Input Example : 80/HTTP , 576/TCP , 0/ICMP , LDAP"""
        self.Input = Input
        if '/' in self.Input :
            self.Number , self.Protocol = self.Input.strip().split('/',1)
            self.Protocol = self.Protocol.upper()
            try    : self.Number = int(self.Number)
            except : self.Number = 0
        else :
            self.Number   = Get.Port_Number(self.Input)
            self.Protocol = self.Input if Validate.Port(self.Number) else ''

        self.Validate()

        if self.Valid :
            self.Type          = Get.Port_Type(self.Protocol)
            self.Protocol      = self.Protocol
            self.Well_Khown    = Validate.WellKhown(self.Number)
            self.Default       = Validate.DefaultProtocol(self.Number , self.Protocol)

    def Validate (self) -> None :
        if   self.Number == 0 and self.Protocol.upper() == 'ICMP'                  : self.Valid = True
        elif self.Number != 0 and self.Protocol.upper() == 'ICMP'                  : self.Valid = False
        elif Validate.Port(self.Number) and Validate.Protocol(self.Protocol) : self.Valid = True
        else                                                                       : self.Valid = False

    def __str__ (self) -> str :
        return f'{self.Number}/{self.Protocol}' if self.Valid else self.Input
    
    def __bool__ (self) -> str :
        return self.Valid

class Addr :
    def __init__(self , Input : str) -> None :

        self.Input = Input.strip()

        if ':' in Input :
            i , j = Input.split(':',1)
            self.IP   = IPv4(i.strip())
            self.Port = Port(j.strip())
        else :
            self.IP   = ''
            self.Port = ''

        self.Validate()

    def Validate (self) -> None :
        self.Valid = True if self.IP and self.Port else False

    def __str__ (self) -> str :
        return f'{self.IP.IPv4}:{self.Port.Number}' if self.Valid else self.Input

    def __bool__ (self) -> bool :
        return self.Valid

class Hostname : # not compleate
    def __init__(self,Hostname) -> None:
        self.Hostname = Hostname