from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.validator import FQDN,EnglishSpecial,Hostname

class Node(InfoMixin, OwnerMixin):
    __tablename__      = 'nodes'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hostname           = Column(String, nullable=False, info={'Validator':(EnglishSpecial,Hostname)})
    fqdn               = Column(String, nullable=False, info={'Validator':(EnglishSpecial,FQDN)})

    company            = relationship("Company", back_populates="nodes")
    company_id         = Column(Integer, ForeignKey('companies.id'), nullable=False)

    location           = relationship("Location", back_populates="nodes")
    location_id        = Column(Integer, ForeignKey('locations.id'), nullable=False)