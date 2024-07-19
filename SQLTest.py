if __name__ == '__main__' :
    CONFIGFILE = '.configfiles/config.ini'

    from Class.config import Config
    from Class.component.sqlmanager import SQLManager
    from Model   import Base,Models


    Main_Config = Config(
        Config_File = CONFIGFILE,
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
        Base        = Base ,
        Models      = Models ,
        )
    
    with Main_SQLManager :
        New_User = Main_SQLManager.User(username='admin',password='admin',first_name='Administrator',last_name=' ',email='local@local.local')
        Main_SQLManager.Create(New_User)