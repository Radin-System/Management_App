from .Class        import Config
from .Constant     import CONFIGFILE
from .Class.Logger import Logger

Config_Manager = Config(CONFIGFILE)
Logging = Logger('Main',Config_Manager.Get('GLOBAL','logfile'))