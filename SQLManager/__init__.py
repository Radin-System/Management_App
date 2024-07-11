import sqlalchemy
import sqlalchemy.orm
import os
from Class.Decorator     import Do_Log
from Class.Auth    import Username , Password
from Class.Network import IPv4 , Port
from Class import Component

class SQLAlchemyManager(Component):
    def __init__(self,Name:str,*,
            Host:IPv4,
            Port:Port,
            Username:Username,
            Password:Password,
            DataBase:str,
            Mode:str,
            SQLite_Path:str,
            Verbose:bool,
            ) -> None :

        self.Name        = Name
        self.Host        = Host
        self.Port        = Port
        self.Username    = Username
        self.Password    = Password
        self.DataBase    = DataBase
        self.Mode        = Mode
        self.SQLite_Path = SQLite_Path
        self.Verbose     = Verbose

    def Connected(self) -> bool:
        if self.Engine :
            try    : self.Engine.connect() ; return True
            except : return False
        return False

    @Do_Log('Creating engine...','Done!')
    def Create_Engine(self) :
        if   self.Mode == 'MYSQL'   : self.Engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}',echo=self.Verbose)
        elif self.Mode == 'MSSQL'   : self.Engine = sqlalchemy.create_engine(f'mssql+pyodbc://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}'        ,echo=self.Verbose)
        elif self.Mode == 'POSTGRE' : self.Engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}' ,echo=self.Verbose)
        elif self.Mode == 'MARIADB' : self.Engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.Username.Username}:{self.Password.Raw}@{self.Host.IPv4}:{self.Port.Number}/{self.DataBase}'       ,echo=self.Verbose)
        else                        : self.Engine = sqlalchemy.create_engine(f'sqlite:///{os.path.join(self.SQLite_Path,self.DataBase)}.db'                                                            ,echo=self.Verbose)
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
    def Start_Actions(self):
        pass
    
    @Do_Log('Stopping...','Done!')
    def Stop_Actions(self):
        self.Engine = None