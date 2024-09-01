from sqlalchemy import Boolean, Column, String

from classes.model.mixins import *
from classes.policy.input import *
from classes.validator import EnglishSpecial, Uuid

class User(BaseMixin, PasswordMixin, IdMixin, NameMixin, FlagMixin, AuditMixin, UserMixin):
    __tablename__ = 'users'
    username      = Column(String, nullable=False, unique=True, info={'Policy':UsernamePolicy})
    position      = Column(String, nullable=True, info={'Policy':NamePolicy_En})
    avatar_path   = Column(String, default="asset/default/UserAvatar.jpg", nullable=False, info={'Policy':(CleanString + InputPolicy(Name='PathPolicy', Validators=[EnglishSpecial]))})
    sarv_id       = Column(String, nullable=True, unique=True, info={'Policy':(HiddenField + InputPolicy(Name='SarvIdPolicy', Validators=[Uuid]))})
    admin         = Column(Boolean, default=False, nullable=False, info={'Policy':None})
