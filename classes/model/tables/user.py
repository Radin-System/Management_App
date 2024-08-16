from sqlalchemy import Boolean, Column, Integer, String

from classes.model.mixins import *
from classes.validator import EnglishSpecial,Password,Username

class User(UserMixin, NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, nullable=False, unique=True, info={'Validator':(EnglishSpecial,Username)})
    password      = Column(String, nullable=False, info={'Validator':(Password)})
    admin         = Column(Boolean, default=False, nullable=False)
    sarv_id       = Column(String, nullable=True, unique=True)