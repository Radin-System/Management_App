import sqlalchemy
import sqlalchemy.orm
import os
from Global.Constant      import SQLMANAGER_DEBUG , SQLMANAGER_LOG , SQLMANAGER_MODE , SQLMANAGER_VERBOSE , SQLMANAGER_SQLITE_PATH
from Global.Decorator     import Do_Log
from Global.Class.Auth    import User , Password
from Global.Class.Logger  import Logger
from Global.Class.Network import IPv4 , Port

class SQLAlchemyManager :
    def __init__(self , Host : IPv4 , Port : Port , Username : User , Password : Password , DataBase : str):
        self.Logger = Logger('SQL Manager' , SQLMANAGER_LOG , SQLMANAGER_DEBUG)

        self.Host     = Host
        self.Port     = Port
        self.Username = Username
        self.Password = Password
        self.DataBase = DataBase
        self.Mode     = SQLMANAGER_MODE

    def Connected(self) -> bool:
        if self.Engine :
            try    : self.Engine.connect() ; return True
            except : return False
        return False

    @Do_Log('Creating engine...','Done!')
    def Create_Engine(self) :
        if   self.Mode == 'MYSQL'   : self.Engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}',echo=SQLMANAGER_VERBOSE)
        elif self.Mode == 'MSSQL'   : self.Engine = sqlalchemy.create_engine(f'mssql+pyodbc://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}'        ,echo=SQLMANAGER_VERBOSE)
        elif self.Mode == 'POSTGRE' : self.Engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}' ,echo=SQLMANAGER_VERBOSE)
        elif self.Mode == 'MARIADB' : self.Engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}'       ,echo=SQLMANAGER_VERBOSE)
        else                        : self.Engine = sqlalchemy.create_engine(f'sqlite:///{os.path.join(SQLMANAGER_SQLITE_PATH,self.DataBase)}.db'                                                      ,echo=SQLMANAGER_VERBOSE)
        if self.Connected() : self.Base.metadata.create_all(self.Engine)
        else                : self.Logger('Engine Faild')
    
    @Do_Log('Initiating Base','Done!')
    def Init_Base(self , Base) :
        self.Base = Base
    
    @Do_Log('Initiating SQL Models...' , 'Initiation Compleated !')
    def Init_Models(self, Models : list) -> None:
        if self.Base :
            for Model in Models : 
                self.Logger(f'Model : {Model.__name__}')
                setattr(self , Model.__name__ , Model)
        else : self.Logger('faild to Initiate Models : No Base !')

    def Create(self, Instance) -> int :
        try:
            with self.Engine.connect() as Connection:
                with Connection.begin():
                    Session = sqlalchemy.orm.Session(bind=Connection)
                    Session.add(Instance)
                    Session.commit()
                    Session.close()
        except Exception as e:
            self.Logger(f"Error creating record {Instance}")
            if 'Session' in locals() and Session :
                Session.rollback()
                self.Logger("Transaction rolled back.")
                Session.close()
            raise e
        
    def Update(self, Instance) -> None :
        try:
            with self.Engine.connect() as Connection:
                with Connection.begin():
                    Session = sqlalchemy.orm.Session(bind=Connection)
                    Session.merge(Instance)
                    Session.commit()
                    Session.close()
        except Exception as e : 
            self.Logger(f"Error updating record {Instance}")
            if 'Session' in locals() and Session :
                Session.rollback()
                self.Logger("Transaction rolled back.")
                Session.close()
            raise e

    def Delete(self, Instance) -> None :
        try:
            with self.Engine.connect() as Connection:
                with Connection.begin():
                    Session = sqlalchemy.orm.Session(bind=Connection)
                    Session.delete(Instance)
                    Session.commit()
                    Session.close()
        except Exception as e :  
            self.Logger(f"Error deleting record : {e}")
            if 'Session' in locals() and Session :
                Session.rollback()
                self.Logger("Transaction rolled back.")
                Session.close()
            raise e

    def Query(self , 
                Model , 
                Eager  : bool = False,
                Sort   : list = []   ,
                First  : bool = False, 
                Limit  : int  = None , 
                Offset : int  = None , 
                **Conditions) -> (list | None) : #Usage : SQLManager.Query(SQLManager.User , Eager=True , Sort=[('name','asc')] , First = False , Limit = 10 , Offset = 12 , email = None)
        try:
            if not self.Connected() : raise Exception('Not connected to the database.')            
            with self.Engine.connect() as Connection:
                with Connection.begin() :
                    Session = sqlalchemy.orm.Session(bind=Connection)
                    Query   = Session.query(Model)
                    if Eager      : Query = Query.options(sqlalchemy.orm.joinedload('*'))
                    if Conditions : Query = Query.filter_by(**Conditions)
                    if Sort       :
                        for attr, order in Sort :
                            if   order.lower() == 'asc'  : Query = Query.order_by(getattr(Model, attr).asc())
                            elif order.lower() == 'desc' : Query = Query.order_by(getattr(Model, attr).desc())
                            else                         : raise ValueError(f"Invalid sorting order: {order}")
                    if Limit      : Query = Query.limit(Limit)
                    if Offset     : Query = Query.offset(Offset)
                    if First      : Result = Query.first()
                    else          : Result = Query.all()
                    Session.close()
                    return Result
        except Exception as e :
            self.Logger(f"Error executing query: {e}")
            if 'Session' in locals() and Session : Session.close()
            raise e

    def Count(self, Model, **Conditions) -> int:
        try:
            if not self.Connected() : raise Exception('Not connected to the database.')
            with self.Engine.connect() as Connection :
                with Connection.begin():
                    Session = sqlalchemy.orm.Session(bind=Connection)
                    Query   = Session.query(Model)
                    if Conditions : Query = Query.filter_by(**Conditions)
                    return Query.count()
        except Exception as e:
            self.Logger(f"Error executing count query: {e}")
            if 'Session' in locals() and Session : Session.close()
            raise e

    @Do_Log('Starting...','Done!')
    def Start(self):
        if not self.Connected() :
            self.Running = True
    
    @Do_Log('Stopping...','Done!')
    def Stop(self):
        if self.Connected() :
            self.Running = False
            self.Engine = None