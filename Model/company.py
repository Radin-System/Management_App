from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Company(InfoMixin, OwnerMixin):
    __tablename__ = 'companies'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    en_name       = Column(String, nullable=False, unique=True)
    fa_name       = Column(String, nullable=False, unique=True)
    domain        = Column(String, nullable=False, unique=True)
    sarv_uid      = Column(String, nullable=False, unique=True)

    locations     = relationship("Location", back_populates="company")
    personnels    = relationship("Personnel", back_populates="company")
    devices       = relationship("Device", back_populates="company")
    nodes         = relationship("Node", back_populates="company")