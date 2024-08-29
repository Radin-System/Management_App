from sqlalchemy import Column, Integer, String

from classes.policy.input import *

class IdMixin:
    __abstract__ = True
    id           = Column(Integer, primary_key=True, autoincrement=True, info={'Policy':BaseInfoPolicy})
    uid          = Column(String, nullable=True, info={'Policy':UuidPolicy})
