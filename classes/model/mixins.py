from typing import Any
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ._base import Base
from .column_info import *

class BaseMixin(Base):
    __abstract__ = True

    def __setattr__(self, Name:str, Value:Any):
        # Getting the Coloumn
        Column_Object:Column = self.__table__.columns.get(Name)
        Policy:ColumnInfo = Column_Object.info.get('Policy', None)

        if Column_Object is not None: 
            Value = Policy.Apply(Value)

        super().__setattr__(Name, Value)

class InfoMixin:
    __abstract__ = True
    id           = Column(Integer, primary_key=True, autoincrement=True, info={'Policy':BaseInfoPolicy})
    uid          = Column(String, nullable=True, info={'Policy':UuidPolicy})
    description  = Column(Text, nullable=True)
    active       = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    visible      = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    deletable    = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    changable    = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    create_date  = Column(DateTime, default=datetime.now(), nullable=False, info={'Policy':BaseInfoPolicy})
    last_update  = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False, info={'Policy':BaseInfoPolicy})

class NameMixin:
    __abstract__  = True
    firstname_en  = Column(String, nullable=False, info={'Policy':NamePolicy_En})
    lastname_en   = Column(String, nullable=True, info={'Policy':NamePolicy_En})
    firstname_fa  = Column(String, nullable=False, info={'Policy':NamePolicy_Fa})
    lastname_fa   = Column(String, nullable=True, info={'Policy':NamePolicy_Fa})

    def calc_fullname(self) -> None:
        self.fullname_en = f'{self.firstname_en} {self.lastname_en if self.lastname_en is not None else ''}'.strip()
        self.fullname_fa = f'{self.firstname_fa} {self.lastname_fa if self.lastname_fa is not None else ''}'.strip()

class ContactMixin:
    email         = Column(String, nullable=True, info={'Policy':EmailPolicy})
    extension     = Column(Integer, nullable=True, info={'Policy':EnsureInteger})
    mobile_number = Column(String, nullable=True, info={'Policy':MobilePolicy})

class OwnerMixin:
    __abstract__ = True

    @declared_attr
    def owner(cls): 
        return relationship("User", backref=f"owned_{cls.__tablename__}")

    @declared_attr
    def owner_id(cls): 
        return Column(Integer, ForeignKey('users.id'), nullable=False)

__all__ = [
    'BaseMixin',
    'InfoMixin',
    'NameMixin',
    'OwnerMixin',
    'ContactMixin',
    'UserMixin',
]