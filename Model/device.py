from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

class Device(InfoMixin, OwnerMixin):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String, nullable=False)
    type = Column(String, nullable=False)
    connection_method = Column(String, nullable=False)
    connection_port = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    location = relationship("Location", back_populates="devices")