from .Class               import SQLAlchemyManager
from .Models              import Base,Models
from Global               import Main_Config
from Global.Class.Auth    import User , Password
from Global.Class.Network import IPv4 , Port

SQLManager = SQLAlchemyManager('SQLManager',
    Host        = IPv4(Main_Config.Get('SQLMANAGER','host')),
    Port        = Port(Main_Config.Get('SQLMANAGER','port')), 
    Username    = User(Main_Config.Get('SQLMANAGER','username')), 
    Password    = Password(Main_Config.Get('SQLMANAGER','password')),
    DataBase    = Main_Config.Get('SQLMANAGER','database'),
    Mode        = Main_Config.Get('SQLMANAGER','mode'),
    SQLite_Path = Main_Config.Get('SQLMANAGER','sqlite_path'),
    Verbose     = Main_Config.Get('SQLMANAGER','verbose') ,)
SQLManager.Init_Base(Base = Base)
SQLManager.Create_Engine()
SQLManager.Init_Models(Models = Models)