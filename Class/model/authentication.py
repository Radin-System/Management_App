from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import InfoMixin, OwnerMixin

from Class.validator import Username,EnglishSpecial

class Authentication(InfoMixin, OwnerMixin):
    __tablename__ = 'authentications'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    type          = Column(String, nullable=False, unique=True, info={'Validator':EnglishSpecial})
    username      = Column(String, nullable=False, info={'Validator':(EnglishSpecial,Username)})
    password      = Column(String, nullable=False)
    enable        = Column(String, nullable=True)

    devices       = relationship("Device", back_populates="authentication")