from .Class    import Config
from .Class    import Logger
from .Constant import CONFIGFILE

Main_Config = Config(CONFIGFILE)
Main_Logger = Logger(
    Name            = 'Main',
    Log_File        = Main_Config.Get('GLOBALS','log_file'),
    Debug_Condition = Main_Config.Get('GLOBALS','debug'),
    Header          = Main_Config.Get('LOG','log_header'),
    Time_Format     = Main_Config.Get('LOG','log_time_format'),
    )