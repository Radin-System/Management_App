from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

from Class.validator import English, EnglishSpecial,Hostname,FQDN,Ipv4OrFQDN,Port

class Device(InfoMixin, OwnerMixin):
    __tablename__      = 'devices'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hostname           = Column(String, nullable=False, info={'Validator':(EnglishSpecial,Hostname)})
    fqdn               = Column(String, nullable=False, unique=True, info={'Validator':(EnglishSpecial,FQDN)})
    type               = Column(String, nullable=False, info={'Validator':EnglishSpecial})
    management_address = Column(String, nullable=True, info={'Validator':(EnglishSpecial,Ipv4OrFQDN)})
    connection_method  = Column(String, nullable=False, info={'Validator':English})
    connection_port    = Column(Integer, nullable=False, info={'Validator':Port})

    company            = relationship("Company", back_populates="devices")
    company_id         = Column(Integer, ForeignKey('companies.id'), nullable=False)

    location           = relationship("Location", back_populates="devices")
    location_id        = Column(Integer, ForeignKey('locations.id'), nullable=False)

    authentication     = relationship("Authentication", back_populates="devices")
    authentication_id  = Column(Integer, ForeignKey('authentications.id'), nullable=False)