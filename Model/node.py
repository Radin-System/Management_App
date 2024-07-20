from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Node(InfoMixin, OwnerMixin):
    __tablename__      = 'nodes'
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hostname           = Column(String, nullable=False)
    fqdn               = Column(String, nullable=False, unique=True)

    company       = relationship("Company", back_populates="nodes")
    company_id    = Column(Integer, ForeignKey('companies.id'), nullable=False)

    location           = relationship("Location", back_populates="nodes")
    location_id        = Column(Integer, ForeignKey('locations.id'), nullable=False)