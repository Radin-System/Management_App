from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Location(InfoMixin, OwnerMixin):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company", back_populates="locations")
    devices = relationship("Device", back_populates="location")