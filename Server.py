if __name__ == '__main__' :
    CONFIGFILE = '.configfiles/config.ini'

    from classes.config import Config
    from classes.component import *
    from classes.model import Base,Models
    from blueprints import Blueprints

    Main_Config = Config(
        Config_File = CONFIGFILE,
    )

    Main_Logger = Logger(
        Log_File        = Main_Config.Get('GLOBALS','log_file'),
        Debug_Condition = Main_Config.Get('GLOBALS','debug'),
        Header          = Main_Config.Get('LOG','log_header'),
        Time_Format     = Main_Config.Get('LOG','log_time_format'),
    )

    Main_TaskManager = TaskManager(
        Check_Interval = Main_Config.Get('TASKMANAGER','check_interval'),
    )

    Main_SQLManager = SQLManager(
        Host        = Main_Config.Get('SQLMANAGER','host'),
        Port        = Main_Config.Get('SQLMANAGER','port'),
        Username    = Main_Config.Get('SQLMANAGER','username'),
        Password    = Main_Config.Get('SQLMANAGER','password'),
        DataBase    = Main_Config.Get('SQLMANAGER','database'),
        Mode        = Main_Config.Get('SQLMANAGER','mode'),
        SQLite_Path = Main_Config.Get('SQLMANAGER','sqlite_path'),
        Verbose     = Main_Config.Get('SQLMANAGER','verbose'),
        Base        = Base,
        Models      = Models,
    )

    Main_AMIManager = AMIManager(
        Host            = Main_Config.Get('AMIMANAGER','host'),
        Port            = Main_Config.Get('AMIMANAGER','port'),
        Username        = Main_Config.Get('AMIMANAGER','username'),
        Password        = Main_Config.Get('AMIMANAGER','password'),
        Event_Whitelist = Main_Config.Get('AMIMANAGER','event_whitelist_csv'),
        Timeout         = Main_Config.Get('AMIMANAGER','timeout'),
        Max_ActionID    = Main_Config.Get('AMIMANAGER','max_action_id'),
    )

    Main_Webserver = WebServer(
        Host            = Main_Config.Get('WEBSERVER','host'),
        Port            = Main_Config.Get('WEBSERVER','port'),
        Flask_Debug     = Main_Config.Get('WEBSERVER','flask_debug'),
        Secret_Key      = Main_Config.Get('WEBSERVER','secret_key'),
        Blueprints      = Blueprints,
    )