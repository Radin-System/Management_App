from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.validator import English,Domain,EnglishSpecial,Persian,PhoneNumber

class Company(InfoMixin, OwnerMixin):
    __tablename__ = 'companies'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    en_name       = Column(String, nullable=False, unique=True, info={'Validator':English})
    fa_name       = Column(String, nullable=False, unique=True, info={'Validator':Persian})
    domain        = Column(String, nullable=False, unique=True, info={'Validator':(EnglishSpecial,Domain)})
    phone_number  = Column(String, nullable=True, unique=True, info={'Validator':PhoneNumber})
    sarv_uid      = Column(String, nullable=True, unique=True)

    locations     = relationship("Location", back_populates="company")
    personnels    = relationship("Personnel", back_populates="company")
    devices       = relationship("Device", back_populates="company")
    nodes         = relationship("Node", back_populates="company")