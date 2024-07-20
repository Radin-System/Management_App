from sqlalchemy.ext.declarative import declarative_base,declared_attr
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class NameMixin(Base):
    __abstract__ = True
    en_firstname = Column(String, nullable=False)
    en_lastname  = Column(String, nullable=False)
    fa_firstname = Column(String, nullable=False)
    fa_lastname  = Column(String, nullable=False)
    email        = Column(String, nullable=True)
    extension    = Column(Integer, nullable=True)
    phone_number = Column(String, nullable=True)
    
class InfoMixin(Base):
    __abstract__ = True
    description  = Column(Text, nullable=True)
    create_date  = Column(DateTime, default=datetime.now())
    last_update  = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    active       = Column(Boolean, default=True)
    deletable    = Column(Boolean, default=True)
    changable    = Column(Boolean, default=True)
    visible      = Column(Boolean, default=True)

class OwnerMixin:
    __abstract__ = True

    @declared_attr
    def owner_id(cls): return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def owner(cls): return relationship("User", backref=f"owned_{cls.__tablename__}")

from authentication import Authentication
from .company import Company
from .device import Device
from .location import Location
from .user import User

Models = [
    Authentication,
    Company,
    Device,
    Location,
    User,
    ]