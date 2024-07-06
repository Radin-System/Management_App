from .Class    import Config
from .Class    import Logger
from .Constant import CONFIGFILE

Config_Manager = Config(CONFIGFILE)
Logging = Logger(
                Name            = 'Main',
                LogFile         = Config_Manager.Get('GLOBAL','logfile'),
                Debug_Condition = Config_Manager.Get('GLOBAL','debug'),
                Header          = Config_Manager.Get('LOG','log_header'),
                Time_Format     = Config_Manager.Get('LOG','log_time_format'),
    )