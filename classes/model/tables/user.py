from sqlalchemy import Boolean, Column, Integer, String

from classes.model.mixins import *
from classes.model.coloumn_info import *
from classes.validator import EnglishSpecial, Uuid

class User(UserMixin, NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True, info=(BaseInfoPolicy).Dict())
    username      = Column(String, nullable=False, unique=True, info=(UsernamePolicy).Dict())
    password      = Column(String, nullable=False, info=(PasswordPolicy).Dict())
    position      = Column(String, nullable=True, info=(NamePolicy_En).Dict)
    avatar_path   = Column(String, default="asset/default/UserAvatar.jpg", nullable=False, info=(CleanString + ColoumnInfo(Validators=[EnglishSpecial])).Dict())
    sarv_id       = Column(String, nullable=True, unique=True, info=(HiddenField + ColoumnInfo(Validators=[Uuid])).Dict())
    admin         = Column(Boolean, default=False, nullable=False, info={})
