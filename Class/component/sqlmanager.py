import os,sqlalchemy,sqlalchemy.orm

from Class.component import Component
from Function.decorator import Running_Required,Connection_Required,Return_False_On_Exception

class SQLManager(Component):
    def __init__(self,*,
            Host:str,
            Port:int,
            Username:str,
            Password:str,
            DataBase:str,
            Mode:str,
            SQLite_Path:str,
            Verbose:bool,
            Base,
            Models:list,
            ) -> None :

        self.Host        = Host
        self.Port        = Port
        self.Username    = Username
        self.Password    = Password
        self.DataBase    = DataBase
        self.Mode        = Mode
        self.SQLite_Path = SQLite_Path
        self.Verbose     = Verbose
        self.Base        = Base
        self.Models      = Models

    @Running_Required
    @Return_False_On_Exception
    def Is_Connected(self) -> bool:
        self.Engine.connect()
        return True

    @Running_Required
    def Create_Engine(self):
        if   self.Mode == 'MYSQL'   : self.Engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}',echo=self.Verbose)
        elif self.Mode == 'MSSQL'   : self.Engine = sqlalchemy.create_engine(f'mssql+pyodbc://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}'        ,echo=self.Verbose)
        elif self.Mode == 'POSTGRE' : self.Engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}' ,echo=self.Verbose)
        elif self.Mode == 'MARIADB' : self.Engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}'       ,echo=self.Verbose)
        else                        : self.Engine = sqlalchemy.create_engine(f'sqlite:///{os.path.join(self.SQLite_Path,self.DataBase)}.db'                                   ,echo=self.Verbose)
        self.Base.metadata.create_all(self.Engine)

    @Running_Required
    def Init_Models(self) -> None:
        for Model in self.Models :
            setattr(self , Model.__name__ , Model)

    @Running_Required
    @Connection_Required
    def Create(self, Instance) -> int:
        with self.Engine.connect() as Connection:
            with Connection.begin():
                with sqlalchemy.orm.Session(bind=Connection) as Session:
                    Session.add(Instance)
                    Session.commit()

    @Running_Required
    @Connection_Required
    def Update(self, Instance) -> None:
        with self.Engine.connect() as Connection:
            with Connection.begin():
                with sqlalchemy.orm.Session(bind=Connection) as Session:
                    Session.merge(Instance)
                    Session.commit()

    @Running_Required
    @Connection_Required
    def Delete(self, Instance) -> None:
        with self.Engine.connect() as Connection:
            with Connection.begin():
                with sqlalchemy.orm.Session(bind=Connection) as Session:
                    Session.delete(Instance)
                    Session.commit()

    @Running_Required
    @Connection_Required
    def Query(self,Model,*, 
        Eager:bool = False,
        Sort:list[tuple[str,str]] = [],
        First:bool = False, 
        Limit:int = None, 
        Offset:int = None,
        **Conditions
        ) -> (list | None): 
        #Usage : SQLManager.Query(SQLManager.User , Eager=True , Sort=[('name','asc')] , First = False , Limit = 10 , Offset = 12 , email = None)
      
        with self.Engine.connect() as Connection:
            with Connection.begin():
                with sqlalchemy.orm.Session(bind=Connection) as Session:
                    Query   = Session.query(Model)
                    if Eager      : Query = Query.options(sqlalchemy.orm.joinedload('*'))
                    if Conditions : Query = Query.filter_by(**Conditions)
                    if Sort       :
                        for attr, order in Sort :
                            if   'asc'  in order.lower(): Query = Query.order_by(getattr(Model, attr).asc())
                            elif 'desc' in order.lower(): Query = Query.order_by(getattr(Model, attr).desc())
                            else                        : raise ValueError(f"Invalid sorting order: {order}")
                    if Limit  : Query = Query.limit(Limit)
                    if Offset : Query = Query.offset(Offset)
                    if First  : Result = Query.first()
                    else      : Result = Query.all()
                    return Result

    @Running_Required
    @Connection_Required
    def Count(self, Model, **Conditions) -> int:
        with self.Engine.connect() as Connection:
            with Connection.begin():
                with sqlalchemy.orm.Session(bind=Connection) as Session:
                    Query   = Session.query(Model)
                    if Conditions : Query = Query.filter_by(**Conditions)
                    return Query.count()

    def Start_Actions(self) -> None:
        self.Create_Engine()
        self.Init_Models()
    
    def Stop_Actions(self) -> None:
        self.Engine = None