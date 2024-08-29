from sqlalchemy import Column, DateTime, Text, func

from classes.policy.input import *

class AuditMixin:
    __abstract__ = True
    description  = Column(Text, nullable=True)
    create_date  = Column(DateTime, default=func.now(), nullable=False, info={'Policy':BaseInfoPolicy})
    last_update  = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, info={'Policy':BaseInfoPolicy})
