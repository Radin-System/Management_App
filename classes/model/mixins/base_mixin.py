from typing import Any
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseMixin(Base):
    __abstract__ = True

    def __setattr__(self, Name:str, Value:Any):
        # Getting the Coloumn
        Column_Object = self.__table__.columns.get(Name)

        if Column_Object is not None: 
            Policy = Column_Object.info.get('Policy', None)

            if Policy is not None:
                Value = Policy.Apply(Value)

        super().__setattr__(Name, Value)
