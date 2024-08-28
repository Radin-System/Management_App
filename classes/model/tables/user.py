from sqlalchemy import Boolean, Column, Integer, String

from classes.model.mixins import *
from classes.model.coloumn_info import *
from classes.validator import EnglishSpecial, Uuid

class User(UserMixin, NameMixin, InfoMixin):
    __tablename__ = 'users'
    username      = Column(String, nullable=False, unique=True, info={'Policy':UsernamePolicy})
    password      = Column(String, nullable=False, info={'Policy':PasswordPolicy})
    position      = Column(String, nullable=True, info={'Policy':NamePolicy_En})
    avatar_path   = Column(String, default="asset/default/UserAvatar.jpg", nullable=False, info={'Policy':(CleanString + ColoumnInfo(Validators=[EnglishSpecial]))})
    sarv_id       = Column(String, nullable=True, unique=True, info={'Policy':(HiddenField + ColoumnInfo(Validators=[Uuid]))})
    admin         = Column(Boolean, default=False, nullable=False, info={'Policy':None})
