from sqlalchemy import Boolean, Column, Integer, String
from . import InfoMixin,NameMixin

from Class.validator import EnglishSpecial,Password,Username

class User(NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, nullable=False, unique=True, info={'Validator':(EnglishSpecial,Username)})
    password      = Column(String, nullable=False, info={'Validator':(Password)})
    admin         = Column(Boolean, default=False, nullable=False)
    sarv_id       = Column(String, nullable=True, unique=True)