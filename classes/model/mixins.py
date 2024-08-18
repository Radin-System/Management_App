from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from classes.validator import English, EnglishSpecial, Persian, Email, MobileNumber
from ._base import Base
from functions.convert import CleanStr
class InfoMixin(Base):
    __abstract__ = True
    description  = Column(Text, nullable=True)
    active       = Column(Boolean, default=True, nullable=False)
    visible      = Column(Boolean, default=True, nullable=False)
    deletable    = Column(Boolean, default=True, nullable=False)
    changable    = Column(Boolean, default=True, nullable=False)
    create_date  = Column(DateTime, default=datetime.now(), nullable=False)
    last_update  = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __setattr__(self, Name, Value):
        # Getting the Coloumn
        Seting_Column:Column = self.__table__.columns.get(Name)

        if Seting_Column is not None:
            # Cheking Flags
            Flags:dict = Seting_Column.info.get('Flags',None)
            if Flags :
                Changeble = Flags.get('Changeble',None)
                if Changeble == False:
                    raise PermissionError(f'This coloumn is not changble: {Name}')

            # Applying Validators
            Validators:list = Seting_Column.info.get('Validators',None) 
            if Validators:
                for Validator in Validators:
                    Validator(Value)

            # Applying Convertors
            Convertors:list = Seting_Column.info.get('Convertors',None)
            if Convertors:
                for Covertor in Convertors:
                    Value = Covertor(Value)

        super().__setattr__(Name, Value)

class NameMixin:
    __abstract__  = True
    firstname_en  = Column(String, nullable=False, info={'Validators':[English], 'Convertor':[CleanStr]})
    lastname_en   = Column(String, nullable=False, info={'Validators':[English], 'Convertor':[CleanStr]})
    firstname_fa  = Column(String, nullable=False, info={'Validators':[Persian], 'Convertor':[CleanStr]})
    lastname_fa   = Column(String, nullable=False, info={'Validators':[Persian], 'Convertor':[CleanStr]})
    email         = Column(String, nullable=True, info={'Validators':[EnglishSpecial, Email], 'Convertor':[CleanStr]})
    extension     = Column(Integer, nullable=True, info={'Convertor':[int]})
    mobile_number = Column(String, nullable=True,info={'Validators':[MobileNumber], 'Convertor':[CleanStr]})

class OwnerMixin:
    __abstract__ = True

    @declared_attr
    def owner(cls): return relationship("User", backref=f"owned_{cls.__tablename__}")

    @declared_attr
    def owner_id(cls): return Column(Integer, ForeignKey('users.id'), nullable=False)

__all__ = [
    'InfoMixin',
    'NameMixin',
    'OwnerMixin',
    'UserMixin',
]