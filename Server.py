if __name__ == '__main__' :
    from Global.Class    import Config
    from Global.Class    import Logger
    from Global.Constant import CONFIGFILE
    
    from TaskManager import SimpleTaskManager
    
    from SQLManager        import SQLAlchemyManager
    from SQLManager.Models import Base,Models

    from AMIManager import AsteriskAMIManager
    
    Main_Config = Config(
        Config_File = CONFIGFILE,
        )

    Main_Logger = Logger(
        Name            = 'Main',
        Log_File        = Main_Config.Get('GLOBALS','log_file'),
        Debug_Condition = Main_Config.Get('GLOBALS','debug'),
        Header          = Main_Config.Get('LOG','log_header'),
        Time_Format     = Main_Config.Get('LOG','log_time_format'),
        )

    TaskManager = SimpleTaskManager('TaskManager',
        Check_Interval = Main_Config.Get('TASKMANAGER','chck_interval'),
        )
    
    SQLManager = SQLAlchemyManager('SQLManager',
        Host        = Main_Config.Get('SQLMANAGER','host'),
        Port        = Main_Config.Get('SQLMANAGER','port'), 
        Username    = Main_Config.Get('SQLMANAGER','username'), 
        Password    = Main_Config.Get('SQLMANAGER','password'),
        DataBase    = Main_Config.Get('SQLMANAGER','database'),
        Mode        = Main_Config.Get('SQLMANAGER','mode'),
        SQLite_Path = Main_Config.Get('SQLMANAGER','sqlite_path'),
        Verbose     = Main_Config.Get('SQLMANAGER','verbose'),
        )
    SQLManager.Init_Base(Base = Base)
    SQLManager.Create_Engine()
    SQLManager.Init_Models(Models = Models)

    AMIManager = AsteriskAMIManager('AMIManager',
        Host            = Main_Config.Get('AMIMANAGER','host'),
        Port            = Main_Config.Get('AMIMANAGER','port'),
        Username        = Main_Config.Get('AMIMANAGER','username'),
        Password        = Main_Config.Get('AMIMANAGER','password'),
        Event_Whitelist = Main_Config.Get('AMIMANAGER','event_whitelist_csv'),
        Timeout         = Main_Config.Get('AMIMANAGER','timeout'),
        Max_ActionID    = Main_Config.Get('AMIMANAGER','max_action_id'),
        )