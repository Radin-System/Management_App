from sqlalchemy import Column, Boolean
from classes.policy.input import *

class FlagMixin:
    __abstract__ = True
    active       = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    visible      = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    deletable    = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
    changable    = Column(Boolean, default=True, nullable=False, info={'Policy':HiddenField})
