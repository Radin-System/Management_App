from flask_login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ._base import Base
from .coloumn_info import *

class InfoMixin(Base):
    __abstract__ = True
    description  = Column(Text, nullable=True)
    active       = Column(Boolean, default=True, nullable=False, info=(HiddenField).Dict())
    visible      = Column(Boolean, default=True, nullable=False, info=(HiddenField).Dict())
    deletable    = Column(Boolean, default=True, nullable=False, info=(HiddenField).Dict())
    changable    = Column(Boolean, default=True, nullable=False, info=(HiddenField).Dict())
    create_date  = Column(DateTime, default=datetime.now(), nullable=False, info=(BaseInfoPolicy).Dict())
    last_update  = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False, info=(BaseInfoPolicy).Dict())

    def __setattr__(self, Name, Value):
        # Getting the Coloumn
        Set:Column = self.__table__.columns.get(Name)

        if Set is not None: 
            # Applying Modifires
            Setattr:dict = Set.info.get('Setattr')
            if Setattr:
                # Applying Validators
                Validators:list = Setattr.get('Validators',None)
                if Validators:
                    for Validator in Validators:
                        Validator(Value)

                # Applying Convertors
                Convertors:list = Setattr.get('Convertors',None)
                if Convertors:
                    for Covertor in Convertors:
                        Value = Covertor(Value)

        super().__setattr__(Name, Value)

class NameMixin:
    __abstract__  = True
    firstname_en  = Column(String, nullable=False, info=(NamePolicy_En).Dict())
    lastname_en   = Column(String, nullable=False, info=(NamePolicy_En).Dict())
    firstname_fa  = Column(String, nullable=False, info=(NamePolicy_Fa).Dict())
    lastname_fa   = Column(String, nullable=False, info=(NamePolicy_Fa).Dict())
    email         = Column(String, nullable=True, info=(EmailPolicy).Dict())
    extension     = Column(Integer, nullable=True, info=(EnsureInteger).Dict())
    mobile_number = Column(String, nullable=True,info=(MobilePolicy).Dict())

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