
class LDAPUser :
    def __init__(self, userPrincipal : Email, Password : Password, LDAP_Port : Port = None, Use_SSL = None , Validate_SSL = None) :
        self.Exceptions     = []
        self.userPrincipal  = userPrincipal
        self.Password       = Password
        self.Use_SSL        = Use_SSL
        self.Validate_SSL   = Validate_SSL
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
                tls = ldap3.Tls(validate = ssl.CERT_REQUIRED if self.Validate_SSL else ssl.CERT_NONE) , 
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
