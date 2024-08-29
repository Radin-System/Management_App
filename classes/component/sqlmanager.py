import os,sqlalchemy,sqlalchemy.orm
from typing import Any

from classes.policy.input import InputPolicy
from ._base import Component
from functions.decorator import Running_Required

class SQLManager(Component):
    def __init__(self,Name:str,*,
            Base:Any,
            Models:dict,
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
        for Name, Model in self.Models.items() :
            setattr(self, Name, Model)

    @Running_Required
    def Create(self, Instance,*,
        Detached:bool = False
        ) -> None:

        with self.SessionMaker(Detached=Detached) as Session:
            try:
                Session.add(Instance)
                Session.commit()
                self.Logger(f'Creating {Instance} in SQL', 'debug')
            except Exception as e:
                Session.rollback()
                self.Logger('Transaction rolledback','error')
                raise e

    @Running_Required
    def Update(self, Instance,*,
        Detached:bool = False,
        ) -> None:

        if not Instance.changable:
            raise PermissionError(f'this instance is not changable: {Instance}')

        for Column in Instance.__class__.__table__.columns:
            if Column is not None:
                # Cheking Flags
                Policy:InputPolicy = Column.info.get('Policy',None)
                if Policy:
                    if Policy.Changeable == False:
                        raise PermissionError(f'This coloumn is not changeable: {Column}')

        with self.SessionMaker(Detached=Detached) as Session:
            try:
                Session.merge(Instance)
                Session.commit()
                self.Logger(f'Updating {Instance} in SQL', 'debug')
            except Exception as e:
                Session.rollback()
                self.Logger('Transaction rolledback','error')
                raise e

    @Running_Required
    def Delete(self, Instance,*,
        Detached:bool = False,
        ) -> None:

        if not Instance.deletable:
            raise PermissionError(f'this instance is not Deletable: {Instance}')

        with self.SessionMaker(Detached=Detached) as Session:
            try:
                Session.delete(Instance)
                Session.commit()
                self.Logger(f'Deleting {Instance} in SQL', 'debug')
            except Exception as e:
                Session.rollback()
                self.Logger('Transaction rolledback','error')
                raise e

    @Running_Required
    def Query(self,Model,*,
        Detached:bool = False,
        Eager:bool = False,
        DictMode:bool = False,
        First:bool = False, 
        Limit:int = None, 
        Offset:int = None,
        **Conditions,
        ) -> list | dict | Any | None:
        """
        Usage: SQLManager.Query(SQLManager.User,
            Detached = False,
            Eager = True,
            DictMode = False,
            First = False,
            Limit = 10,
            Offset = 12,
            name__sort = 'asc',
            name__like = 'mohammad',
            email = None,
            )
        """
        # Creating Session and getting Query
        with self.SessionMaker(Detached=Detached) as Session:
            try:
                Query = Session.query(Model)

                # Apply eager loading if requested
                if Eager:
                    Query = Query.options(sqlalchemy.orm.joinedload('*'))

                # Apply filtering conditions
                if Conditions:
                    Like_Conditions = {}
                    Exact_Conditions = {}
                    Sort_Conditions = {}

                    # Separate LIKE conditions from exact conditions
                    for Key, Value in Conditions.items():
                        if '__sort' in Key:
                            Sort_Key = Key.replace('__sort', '')
                            Sort_Conditions[Sort_Key] = Value

                        elif '__like' in Key:
                            Like_Key = Key.replace('__like', '')
                            Like_Conditions[Like_Key] = Value

                        else:
                            if hasattr(Model, Key): Exact_Conditions[Key] = Value
                            else: self.Logger(f'the model {Model} does not contain this key: {Key}','warning')

                    # Apply SORT conditions
                    for Key, Value in Sort_Conditions.items():
                        if Value == 'asc': Query = Query.order_by(getattr(Model, Key).asc())
                        if Value == 'desc': Query = Query.order_by(getattr(Model, Key).desc())
                        else: raise ValueError(f"Invalid sorting order: {Value}")

                    # Apply LIKE conditions
                    for Key, Value in Like_Conditions.items():
                        if hasattr(Model, Key): Query = Query.filter(getattr(Model, Key).like(f'%{Value}%'))
                        else: raise AttributeError(f'{Key} is not a valid attribute of {Model}')

                    # Apply EQUAL match conditions
                    if Exact_Conditions:
                        Query = Query.filter_by(**Exact_Conditions)

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
            
            except Exception as e:
                self.Logger('unable executing the query','error')
                raise e

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
        return sqlalchemy.orm.Session(bind=self.Engine, expire_on_commit=Detached)

    def Loop(self) -> None:
        ...

    def Start_Actions(self) -> None:
        pass

    def Stop_Actions(self) -> None:
        pass