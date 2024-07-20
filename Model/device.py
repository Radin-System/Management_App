from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Device(InfoMixin, OwnerMixin):
    __tablename__      = 'devices'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hostname           = Column(String, nullable=False)
    fqdn               = Column(String, nullable=False, unique=True)
    type               = Column(String, nullable=False)
    management_address = Column(String, nullable=True)
    connection_method  = Column(String, nullable=False)
    connection_port    = Column(Integer, nullable=False)

    company            = relationship("Company", back_populates="devices")
    company_id         = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    location           = relationship("Location", back_populates="devices")
    location_id        = Column(Integer, ForeignKey('locations.id'), nullable=False)
    
    authentication     = relationship("Authentication", back_populates="devices")
    authentication_id  = Column(Integer, ForeignKey('authentication.id'), nullable=False)