from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import InfoMixin,NameMixin

class Personnel(InfoMixin,NameMixin):
    __tablename__ = 'personnels'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, nullable=False, unique=True)

    company       = relationship("Company", back_populates="personnels")
    company_id    = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    company       = relationship("Location", back_populates="personnels")
    location_id   = Column(Integer, ForeignKey('location.id'), nullable=False)
    