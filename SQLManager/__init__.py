from .Class               import SQLAlchemyManager
from .Models              import Base,Models
from Global               import Main_Config


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