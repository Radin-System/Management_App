import os,re

ROOT       = os.getcwd()


SPECIAL_CHARS = '!@#$%^&*()_+"|\\/<>?:;{}[]' + "'"

MAC_PATTERN_MAP = {
    'Hex'    : re.compile(r'^[0-9a-f]{12}$'                       , re.IGNORECASE) , # 1234ABCD5678
    'Dotted' : re.compile(r'^([0-9a-f]{4}[.:-]){2}([0-9a-f]{4})$' , re.IGNORECASE) , # 1234.abcd.5678
    'Dubble' : re.compile(r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$'  , re.IGNORECASE) , # 12:34:abcd:56:78
}

CIDR_MAP = {
    '255.255.255.255':'/32','255.255.255.254':'/31','255.255.255.252':'/30','255.255.255.248':'/29','255.255.255.240':'/28','255.255.255.224':'/27','255.255.255.192':'/26','255.255.255.128':'/25',
    '255.255.255.0'  :'/24','255.255.254.0'  :'/23','255.255.252.0'  :'/22','255.255.248.0'  :'/21','255.255.240.0'  :'/20','255.255.224.0'  :'/19','255.255.192.0'  :'/18','255.255.128.0'  :'/17',
    '255.255.0.0'    :'/16','255.254.0.0'    :'/15','255.252.0.0'    :'/14','255.248.0.0'    :'/13','255.240.0.0'    :'/12','255.224.0.0'    :'/11','255.192.0.0'    :'/10','255.128.0.0'    :'/9' ,
    '255.0.0.0'      :'/8' ,'254.0.0.0'      :'/7' ,'252.0.0.0'      :'/6' ,'248.0.0.0'      :'/5' ,'240.0.0.0'      :'/4' ,'224.0.0.0'      :'/3' ,'192.0.0.0'      :'/2' ,'128.0.0.0'      :'/1' ,
    '0.0.0.0'        :'/0' ,
}

MASK_MAP = {
    v : k for k , v in CIDR_MAP.items()
    }

PORT_MAP = {
    'FTP'    : { 'Default_Number' : 21   , 'Type' : ['TCP','SCTP']       , 'Well_Khown' : True  , 'Name' : 'File Transfer Protocol'} ,
    'SSH'    : { 'Default_Number' : 22   , 'Type' : ['TCP','SCTP']       , 'Well_Khown' : True  , 'Name' : 'Secure Shell'} ,
    'TELNET' : { 'Default_Number' : 23   , 'Type' : ['TCP','SCTP']       , 'Well_Khown' : True  , 'Name' : 'Telnet'} ,
    'SMTP'   : { 'Default_Number' : 25   , 'Type' : ['TCP','SCTP']       , 'Well_Khown' : True  , 'Name' : 'Simple Mail Transfer Protocol'} ,
    'DNS'    : { 'Default_Number' : 53   , 'Type' : ['TCP','UDP']        , 'Well_Khown' : True  , 'Name' : 'Domain Name System'} ,
    'TFTP'   : { 'Default_Number' : 69   , 'Type' : ['UDP']              , 'Well_Khown' : True  , 'Name' : 'Trivial File Transfer Protocol'} ,
    'HTTP'   : { 'Default_Number' : 80   , 'Type' : ['TCP','UDP','SCTP'] , 'Well_Khown' : True  , 'Name' : 'Hypertext Transfer Protocol'} ,
    'POP3'   : { 'Default_Number' : 110  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Post Office Protocol'} ,
    'NTP'    : { 'Default_Number' : 123  , 'Type' : ['TCP','UDP']        , 'Well_Khown' : True  , 'Name' : 'Network Time Protocol'} ,
    'IMAP4'  : { 'Default_Number' : 143  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Internet Message Access Protocol'} ,
    'SNMP'   : { 'Default_Number' : 161  , 'Type' : ['UDP']              , 'Well_Khown' : True  , 'Name' : 'Simple Network Management Protocol'} ,
    'SNMPt'  : { 'Default_Number' : 162  , 'Type' : ['TCP','UDP']        , 'Well_Khown' : True  , 'Name' : 'Simple Network Management Protocol Trap'} ,
    'LDAP'   : { 'Default_Number' : 389  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Lightweight Directory Access Protocol'} ,
    'HTTPS'  : { 'Default_Number' : 443  , 'Type' : ['TCP','UDP','SCTP'] , 'Well_Khown' : True  , 'Name' : 'Hypertext Transfer Protocol Secure'} ,
    'ESMTP'  : { 'Default_Number' : 587  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Email Message Submission'} ,
    'LDAPS'  : { 'Default_Number' : 636  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Lightweight Directory Access Protocol over TLS/SSL'} ,
    'MSE'    : { 'Default_Number' : 691  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'MicroSoft Exchange'} ,
    'FTPS'   : { 'Default_Number' : 990  , 'Type' : ['TCP','UDP']        , 'Well_Khown' : True  , 'Name' : 'File Transfer Protocol over TLS/SSL'} ,
    'IMAPS'  : { 'Default_Number' : 993  , 'Type' : ['TCP']              , 'Well_Khown' : True  , 'Name' : 'Internet Message Access Protocol over TLS/SSL'} ,
    'POP3S'  : { 'Default_Number' : 995  , 'Type' : ['TCP','UDP']        , 'Well_Khown' : True  , 'Name' : 'Post Office Protocol Version 3 over TLS/SSL'} ,
    'OVPN'   : { 'Default_Number' : 1194 , 'Type' : ['TCP','UDP']        , 'Well_Khown' : False , 'Name' : 'OpenVPN'} ,
    'MYSQL'  : { 'Default_Number' : 3306 , 'Type' : ['TCP']              , 'Well_Khown' : False , 'Name' : 'MySQL database system'} ,
    'RDP'    : { 'Default_Number' : 3389 , 'Type' : ['TCP','UDP']        , 'Well_Khown' : False , 'Name' : 'Microsoft Terminal Server'} ,
    'WINBOX' : { 'Default_Number' : 8291 , 'Type' : ['TCP']              , 'Well_Khown' : False , 'Name' : 'Mikrotik Management Port'} ,
}

PORT_TYPE_MAP = {
    'UDP'  : {'Name' : 'User Datagram Protocol'} ,
    'TCP'  : {'Name' : 'Transmission Control Protocol'} ,
    'SCTP' : {'Name' : 'Stream Control Transmission Protocol'} , 
    'ICMP' : {'Name' : 'Internet Control Message Protocol'} ,
}
