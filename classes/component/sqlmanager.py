import os,sqlalchemy,sqlalchemy.orm
from typing import Any
from functools import wraps
from classes.model import ModelsTyping
from ._base import Component
from functions.decorator import Running_Required,Connection_Required,Return_False_On_Exception

class SQLManager(Component, ModelsTyping):
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

        self.Connection = None
        self.Session = None

        self.__typing__()
        self.Create_Engine()
        self.Init_Models()

    def Create_Engine(self):
        if   self.Mode == 'MYSQL'   : self.Engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}',echo=self.Verbose)
        elif self.Mode == 'MSSQL'   : self.Engine = sqlalchemy.create_engine(f'mssql+pyodbc://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}'        ,echo=self.Verbose)
        elif self.Mode == 'POSTGRE' : self.Engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}' ,echo=self.Verbose)
        elif self.Mode == 'MARIADB' : self.Engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.Username}:{self.Password}@{self.Host}:{self.Port}/{self.DataBase}'       ,echo=self.Verbose)
        else                        : self.Engine = sqlalchemy.create_engine(f'sqlite:///{os.path.join(self.SQLite_Path,self.DataBase)}.db'                                   ,echo=self.Verbose)
        self.Base.metadata.create_all(self.Engine)

    def Init_Models(self) -> None:
        for Model in self.Models :
            setattr(self , Model.__name__ , Model)

    @Running_Required
    @Return_False_On_Exception
    def Is_Connected(self) -> bool:
        self.Engine.connect()
        return True

    @staticmethod
    def Transaction(Function) -> callable:
        @wraps(Function)
        def Wrapper(*Args,**Kwargs) :
            try:
                result = Function(*Args, **Kwargs)
                Args[0].Session.commit()
                return result
            except Exception as e:
                Args[0].Session.rollback()
                raise e
        return Wrapper

    @Transaction
    @Running_Required
    @Connection_Required
    def Create(self, Instance) -> None:
        self.Session.add(Instance)

    @Transaction
    @Running_Required
    @Connection_Required
    def Update(self, Instance) -> None:
        if not Instance.changable:
            raise PermissionError(f'this instance is not changable: {Instance}')
        
        for Coloumn in Instance.__class__.__table__.columns:
            if Coloumn is not None:
                # Cheking Flags
                Flags:dict = Coloumn.info.get('Flags',None)
                if Flags :
                    Changeble = Flags.get('Changeable',None)
                    if Changeble == False:
                        raise PermissionError(f'This coloumn is not changeable: {Coloumn}')

        self.Session.merge(Instance)

    @Transaction
    @Running_Required
    @Connection_Required
    def Delete(self, Instance) -> None:
        if not Instance.deletable:
            raise PermissionError(f'this instance is not Deletable: {Instance}')
        
        self.Session.delete(Instance)

    @Transaction
    @Running_Required
    @Connection_Required
    def Query(self,Model,*, 
        Eager:bool = False,
        DictMode:bool = False,
        Sort:list[tuple[str,str]] = [],
        First:bool = False, 
        Limit:int = None, 
        Offset:int = None,
        **Conditions
        ) -> list|Any|None:
        #Usage : SQLManager.Query(SQLManager.User , Eager=True , Sort=[('name','asc')] , First = False , Limit = 10 , Offset = 12 , email = None)
        
        # Create the initial query
        Query   = self.Session.query(Model)
        
        # Apply eager loading if requested
        if Eager: 
            for Relationship in sqlalchemy.inspect(Model).relationships:
                Query = Query.options(sqlalchemy.orm.joinedload(Relationship.key))
        
        # Apply filtering conditions
        if Conditions: 
            Query = Query.filter_by(**Conditions)
        
        # Apply sorting
        if Sort:
            for attr, order in Sort:
                if   'asc'  in order.lower():
                    Query = Query.order_by(getattr(Model, attr).asc())
                elif 'desc' in order.lower():
                    Query = Query.order_by(getattr(Model, attr).desc())
                else:
                    raise ValueError(f"Invalid sorting order: {order}")
        
        # Apply limit and offset
        if Limit: 
            Query = Query.limit(Limit)
        if Offset: 
            Query = Query.offset(Offset)
        
        # Fetch the result
        if First: 
            Result = Query.first()
        else: 
            Result = Query.all()
        
        # Handle detached instances
        if Result and DictMode:
            if First:
                return {col.name: getattr(Result, col.name) for col in Result.__table__.columns}
            else:
                return [{col.name: getattr(instance, col.name) for col in instance.__table__.columns} for instance in Result]
        
        # Return the result
        return Result

    @Transaction
    @Running_Required
    @Connection_Required
    def Count(self, Model, **Conditions) -> int:
        Query = self.Session.query(Model)
        
        if Conditions: 
            Query = Query.filter_by(**Conditions)
        
        return Query.count()

    def Start_Actions(self) -> None:
        self.Connection = self.Engine.connect()
        self.Connection.begin()
        # expire_on_commit: Keeps the instance values in the models instance and dont remove them after commit !
        # This will cause memory intensive app and delay in data collection or data incosistancy
        # Make sure you will implement a way around this
        self.Session = sqlalchemy.orm.Session(bind=self.Connection, expire_on_commit=False) 

    def Stop_Actions(self) -> None:
        self.Session.close()
        self.Connection.close()