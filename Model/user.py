from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import InfoMixin,NameMixin

class User(InfoMixin,NameMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    sarv_id = Column(String, nullable=True, unique=True)