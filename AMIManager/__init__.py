from .Class          import AsteriskAMIManager
from Global import Main_Config

AMIManager = AsteriskAMIManager('AMIManager',
    Host     = Main_Config.Get('AMIMANAGER','host'),
    Port     = Main_Config.Get('AMIMANAGER','port'),
    Username = Main_Config.Get('AMIMANAGER','username'),
    Password = Main_Config.Get('AMIMANAGER','password'),
    Event_Whitelist = Main_Config.Get('AMIMANAGER','event_whitelist_csv'),
    Timeout  =  Main_Config.Get('AMIMANAGER','timeout'),
    )