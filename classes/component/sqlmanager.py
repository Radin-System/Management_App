import os,sqlalchemy,sqlalchemy.orm
from typing import Any
from ._base import Component
from functions.decorator import Running_Required

class SQLManager(Component):
    def __init__(self,Name:str,*,
            Base:Any,
            Models:list,
            ) -> None :

        super().__init__(Name)

        self.Base   = Base
        self.Models = Models        

        self.Process_Type: str = 'Static'

        self.Create_Engine()
        self.Init_Models()

    def Init_Dependancy(self) -> None:
        super().Init_Dependancy()

    def Init_Config(self) -> None:
        self.Host        = self.Config.Get('SQLMANAGER','host')
        self.Port        = self.Config.Get('SQLMANAGER','port')
        self.Username    = self.Config.Get('SQLMANAGER','username')
        self.Password    = self.Config.Get('SQLMANAGER','password')
        self.DataBase    = self.Config.Get('SQLMANAGER','database')
        self.Mode        = self.Config.Get('SQLMANAGER','mode')
        self.SQLite_Path = self.Config.Get('SQLMANAGER','sqlite_path')
        self.Verbose     = self.Config.Get('SQLMANAGER','verbose')

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
    def Create(self, Instance,*,
        Detached:bool = False
        ) -> None:

        Session = self.SessionMaker(Detached=Detached)
        try:
            Session.add(Instance)
            Session.commit()
        except Exception as e:
            Session.rollback()
            raise e

    @Running_Required
    def Update(self, Instance,*,
        Detached:bool = False,
        ) -> None:

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

        Session = self.SessionMaker(Detached=Detached)
        try:
            Session.merge(Instance)
            Session.commit()
        except Exception as e:
            Session.rollback()
            raise e

    @Running_Required
    def Delete(self, Instance,*,
        Detached:bool = False,
        ) -> None:

        if not Instance.deletable:
            raise PermissionError(f'this instance is not Deletable: {Instance}')

        Session = self.SessionMaker(Detached=Detached)
        try:        
            Session.delete(Instance)
            Session.commit()
        except Exception as e:
            Session.rollback()
            raise e

    @Running_Required
    def Query(self,Model,*,
        Detached:bool = False,
        Eager:bool = False,
        DictMode:bool = False,
        Sort:list[tuple[str,str]] = [],
        First:bool = False, 
        Limit:int = None, 
        Offset:int = None,
        **Conditions
        ) -> list|Any|None:
        #Usage : SQLManager.Query(SQLManager.User, Session=SQLManager.SessionMaker(), Eager=True ,Sort=[('name','asc')] ,First = False ,Limit = 10 ,Offset = 12 ,email = None)
        
        # Creating Session and getting Query
        Session = self.SessionMaker(Detached=Detached)
        Query = Session.query(Model)
        
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

    @Running_Required
    def Count(self, Model,*,
        Detached:bool = False,
        **Conditions
        ) -> int:

        Session = self.SessionMaker(Detached=Detached)
        Query = Session.query(Model)
        
        if Conditions: 
            Query = Query.filter_by(**Conditions)
        
        return Query.count()

    @Running_Required
    def SessionMaker(self,*,Detached=False) -> sqlalchemy.orm.Session:
        Connection = self.Engine.connect()
        Connection.begin()
        return sqlalchemy.orm.Session(bind=Connection, expire_on_commit=Detached)

    def Loop(self) -> None:
        ...

    def Start_Actions(self) -> None:
        pass

    def Stop_Actions(self) -> None:
        pass