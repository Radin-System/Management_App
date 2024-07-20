from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Location(InfoMixin, OwnerMixin):
    __tablename__ = 'locations'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    en_name       = Column(String, nullable=False)
    fa_name       = Column(String, nullable=False)

    company       = relationship("Company", back_populates="locations")
    company_id    = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    devices       = relationship("Device", back_populates="location")
    nodes         = relationship("Node", back_populates="location")
    personnels    = relationship("Personnel", back_populates="location")