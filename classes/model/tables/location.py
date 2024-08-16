from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.validator import English, EnglishSpecial, Persian

class Location(InfoMixin, OwnerMixin):
    __tablename__ = 'locations'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    type          = Column(String, nullable=False, info={'Validators':[EnglishSpecial]})
    en_name       = Column(String, nullable=False, info={'Validators':[English]})
    fa_name       = Column(String, nullable=False, info={'Validators':[Persian]})

    company       = relationship("Company", back_populates="locations")
    company_id    = Column(Integer, ForeignKey('companies.id'), nullable=False)

    devices       = relationship("Device", back_populates="location")
    nodes         = relationship("Node", back_populates="location")
    personnels    = relationship("Personnel", back_populates="location")