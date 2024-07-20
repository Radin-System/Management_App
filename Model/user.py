from sqlalchemy import Column, Integer, String
from . import InfoMixin,NameMixin

class User(NameMixin, InfoMixin):
    __tablename__ = 'users'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String, nullable=False, unique=True)
    password      = Column(String, nullable=False)
    sarv_id       = Column(String, nullable=True, unique=True)