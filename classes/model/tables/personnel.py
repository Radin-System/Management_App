from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.validator import EnglishSpecial, Username

class Personnel(NameMixin, InfoMixin, OwnerMixin):
    __tablename__ = 'personnels'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, nullable=False, unique=True, info={'Validators':[EnglishSpecial, Username]})
    agent         = Column(Boolean, nullable=False)

    company       = relationship("Company", back_populates="personnels")
    company_id    = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    location      = relationship("Location", back_populates="personnels")
    location_id   = Column(Integer, ForeignKey('locations.id'), nullable=False)