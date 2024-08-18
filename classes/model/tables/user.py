from sqlalchemy import Boolean, Column, Integer, String
from functions.convert import StrToSha

from classes.model.mixins import *
from classes.validator import EnglishSpecial, Password, Username

class User(UserMixin, NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True, info={'Hidden':True,'Changeable':False})
    username      = Column(String, nullable=False, unique=True, info={'Type':'Username','Validators':[EnglishSpecial, Username]})
    password      = Column(String, nullable=False, info={'Type':'Password','Validators':[Password], 'Convertor':[StrToSha]})
    admin         = Column(Boolean, default=False, nullable=False, info={'Type':'Checkbox'})
    sarv_id       = Column(String, nullable=True, unique=True, info={'Type':'Field','Hidden':True})
