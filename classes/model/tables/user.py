from sqlalchemy import Boolean, Column, Integer, String
from functions.convert import StrToSha, CleanStr

from classes.model.mixins import *
from classes.validator import *

class User(UserMixin, NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True, info={'Hidden':True,'Changeable':False})
    username      = Column(String, nullable=False, unique=True, info={'Type':'Username', 'Validators':[EnglishSpecial, Username], 'Convertor':[CleanStr]})
    password      = Column(String, nullable=False, info={'Type':'Password', 'Validators':[Password], 'Convertor':[StrToSha]})
    position      = Column(String, nullable=True, info={'Hiden':True, 'Type':'Path', 'Validators':[English]})
    avatar_path   = Column(String, nullable=True, info={'Hiden':True, 'Type':'Path', 'Validators':[EnglishSpecial]})
    sarv_id       = Column(String, nullable=True, unique=True, info={'Type':'Field', 'Hidden':True})
    admin         = Column(Boolean, default=False, nullable=False, info={'Type':'Checkbox'})
