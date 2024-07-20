from sqlalchemy.ext.declarative import declarative_base,declared_attr
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from Class.validator import English,EnglishSpecial,Persian,Email,MobileNumber

Base = declarative_base()

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
        Validating_Column:Column = self.__table__.columns.get(Name)
        if Validating_Column is not None:
            Validator = Validating_Column.info.get('Validator',None)
            if Validator :
                if isinstance(Validator,tuple): #Validate by tuple
                    for Item in Validator:
                        Name = Item(Name)

                if isinstance(Validator,type):
                    Name = Validator(Value)

        super().__setattr__(Name, Value)

class NameMixin:
    __abstract__  = True
    en_firstname  = Column(String, nullable=False,info={'Validator':English})
    en_lastname   = Column(String, nullable=False,info={'Validator':English})
    fa_firstname  = Column(String, nullable=False,info={'Validator':Persian})
    fa_lastname   = Column(String, nullable=False,info={'Validator':Persian})
    email         = Column(String, nullable=True,info={'Validator':(EnglishSpecial,Email)})
    extension     = Column(Integer, nullable=True)
    mobile_number = Column(String, nullable=True,info={'Validator':MobileNumber})

class OwnerMixin:
    __abstract__ = True

    @declared_attr
    def owner(cls): return relationship("User", backref=f"owned_{cls.__tablename__}")

    @declared_attr
    def owner_id(cls): return Column(Integer, ForeignKey('users.id'), nullable=False)

from .authentication import Authentication
from .company import Company
from .device import Device
from .location import Location
from .node import Node
from .personnel import Personnel
from .user import User

Models = [
    Authentication,
    Company,
    Device,
    Location,
    Node,
    Personnel,
    User,
    ]