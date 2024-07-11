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
    