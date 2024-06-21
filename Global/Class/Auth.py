import ssl , ldap3
from .Network import Port
from Global.Constant     import ENCODE , SPECIAL_CHARS , LDAPUSER_USE_SSL , LDAPUSER_VALIDATE_SSL
from Global.Function     import Validate , Get , Crypto

class User :
    def __init__(self , Input : str) -> None : 
        self.Input = Input.strip()
        self.Validate()
        self.Username = self.Input if self.Valid else ''

    def Validate(self) -> None :
        self.Valid = bool(Validate.User(self.Input))

    def __str__ (self) -> str :
        return self.Username if self.Valid else self.Input
    
    def __bool__ (self) -> bool :
        return self.Valid

class Password :
    def __init__(self , Input : str ) -> None : 
        self.Input    = Input.strip()
        self.Crypted  = None
        self.MD5      = None
        self.Raw      = None
        self.Method   = None
        self.Score    = 0

        if   Validate.MD5(self.Input)     : self.Method = 'MD5'
        elif Validate.Crypted(self.Input) : self.Method = 'Crypted'
        else                                 : self.Method = 'Raw' 

        if   self.Method == 'MD5'     :
            self.MD5     = self.Input
            self.Crypted = ''
            self.Raw     = ''
        elif self.Method == 'Raw'     : 
            self.MD5     = Crypto.MD5(self.Input)
            self.Crypted = Crypto.Encrypt(self.Input)
            self.Raw     = self.Input
        elif self.Method == 'Crypted' :
            self.MD5     = Crypto.MD5(Crypto.Decrypt(self.Input.encode(ENCODE)))
            self.Crypted = self.Input.encode(ENCODE)
            self.Raw     = Crypto.Decrypt(self.Input)

        self.Validate()

    def Validate(self) -> None :
        if any(char.islower()        for char in self.Raw) : self.Score += 1
        if any(char.isupper()        for char in self.Raw) : self.Score += 1
        if any(char.isdigit()        for char in self.Raw) : self.Score += 1
        if any(char in SPECIAL_CHARS for char in self.Raw) : self.Score += 1
        self.Valid = bool(self.Method == 'MD5' or (self.Score >= 3 and len(self.Raw) >= 7))

    def __str__ (self) -> str :
        return '****'
    
    def __bool__ (self) -> bool :
        return self.Valid

class MD5 :
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        self.Validate()
        if self.Valid : self.MD5 = self.Input

    def Validate(self) -> None:
        self.Valid = Validate.MD5(self.Input)

    def __str__(self) -> str:
        return self.Input
    
    def __bool__(self) -> bool:
        return self.Valid

class Crypted :
    def __init__(self , Input : str) -> None:
        self.Input = Input.strip()
        if isinstance(self.Input,str)   : self.Crypted = self.Input.encode(ENCODE)
        if isinstance(self.Input,bytes) : self.Crypted = self.Input
        self.Validate()
        if not self.Valid : self.Crypted = b''

    def Validate(self) -> None:
        self.Valid = Validate.Crypted(self.Crypted)

    def __str__(self) -> str:
        return self.Input
    
    def __bool__ (self) -> bool:
        return self.Valid

class Domain :
    def __init__(self , DomainName : str ) -> None :
        self.Domain = DomainName.strip()
        self.Validate()
        if self.Valid :
            self.DN            = Get.DN(self.Domain)
            self.LDAP_Endpoint = f'ldap://{self.Domain}'

    def Validate(self) -> None :
        self.Valid = Validate.Domain(self.Domain)

    def __str__ (self) -> str :
        return f'{self.Domain}'
       
    def __bool__ (self) -> bool :
        return self.Valid

class Email:
    def __init__(self , Input : str) -> None : 
        self.Input = Input.strip()
        self.User   = ''
        self.Domain = ''

        if '@' in self.Input :
            Username , DomainName = self.Input.split('@',1)
            self.User   = User(Username)
            self.Domain = Domain(DomainName)

        self.Validate()
        self.Email         = self.Input if self.Valid else ''
        self.userPrincipal = self.Email

    def Validate(self) -> None :
        self.Valid = bool( self.User and self.Domain and Validate.Email(self.Input)) 

    def __str__ (self) -> str :
        return f'{self.User.Username}@{self.Domain.Domain}' if self.Valid else self.Input
    
    def __bool__ (self) -> bool :
        return self.Valid

class Phone :
    def __init__(self , Input : str) -> None:
        self.Input = Input

userPrincipal = Email

class LDAPUser :
    def __init__(self, userPrincipal : userPrincipal, Password : Password, LDAP_Port : Port = None, Use_SSL = LDAPUSER_USE_SSL) :
        self.Exceptions     = []
        self.userPrincipal  = userPrincipal
        self.Password       = Password
        self.Use_SSL        = Use_SSL
        self.Port           = LDAP_Port
        if not self.Port : self.Port = Port('LDAPS') if self.Use_SSL else Port('LDAP')
        self.Validate()
        self.Connect()
        self.Attributes = self.Attributes()

    def Validate (self) -> None :
        self.Valid = bool(self.userPrincipal and self.Port and self.Password and self.Password.Method != 'MD5')

    def Connect(self) -> None :
        if self.Valid :
            Server = ldap3.Server(self.userPrincipal.Domain.LDAP_Endpoint ,
                port = self.Port.Number , 
                use_ssl = self.Use_SSL , 
                tls = ldap3.Tls(validate = ssl.CERT_REQUIRED if LDAPUSER_VALIDATE_SSL else ssl.CERT_NONE) , 
                get_info = ldap3.ALL
                )
            self.Conn = ldap3.Connection(Server , user = self.userPrincipal.userPrincipal , password = self.Password.Raw , auto_bind = True)
        else : self.Conn = None
               
    def Attributes(self) -> dict:
        if self.Conn :
            self.Conn.search(search_base = self.userPrincipal.Domain.DN , search_filter = f'(sAMAccountName = {self.userPrincipal.User.Username})', attributes = ['*'])
            if len(self.Conn.entries) == 0 : return {}
            User_Attributes = {}
            for attr in self.Conn.entries[0].entry_attributes : User_Attributes[attr] = self.Conn.entries[0][attr].value
            return User_Attributes
        return {}

    def __str__(self) -> str :
        return self.userPrincipal.userPrincipal if self.Valid else ''

    def __bool__(self) -> bool :
        return self.Valid
