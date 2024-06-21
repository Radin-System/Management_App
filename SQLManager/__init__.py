from .Class               import SQLAlchemyManager
from .Models              import Base,Models
from sqlalchemy.exc       import IntegrityError
from Global.Constant      import SQLMANAGER_HOST , SQLMANAGER_PORT , SQLMANAGER_USERNAME  , SQLMANAGER_PASSWORD , SQLMANAGER_DATABASE
from Global.Class.Auth    import User , Password
from Global.Class.Network import IPv4 , Port


SQLManager = SQLAlchemyManager(
    Host     = IPv4(SQLMANAGER_HOST),
    Port     = Port(SQLMANAGER_PORT), 
    Username = User(SQLMANAGER_USERNAME), 
    Password = Password(SQLMANAGER_PASSWORD), 
    DataBase = SQLMANAGER_DATABASE 
    )
SQLManager.Name = 'SQLManager'
SQLManager.Init_Base(Base = Base)
SQLManager.Create_Engine()
SQLManager.Init_Models(Models = Models)