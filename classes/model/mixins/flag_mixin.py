from sqlalchemy import Column, Boolean, text
from classes.policy.input import *

class FlagMixin:
    __abstract__ = True
    active       = Column(Boolean, server_default=text('true'), nullable=False, info={'Policy':HiddenField})
    visible      = Column(Boolean, server_default=text('true'), nullable=False, info={'Policy':HiddenField})
    deletable    = Column(Boolean, server_default=text('true'), nullable=False, info={'Policy':HiddenField})
    changable    = Column(Boolean, server_default=text('true'), nullable=False, info={'Policy':HiddenField})
