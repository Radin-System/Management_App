from sqlalchemy import Column, DateTime, Text, text

from classes.policy.input import *

class AuditMixin:
    __abstract__ = True
    description  = Column(Text, nullable=True)
    create_date  = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False, info={'Policy':BaseInfoPolicy})
    last_update  = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"), nullable=False, info={'Policy':BaseInfoPolicy})
