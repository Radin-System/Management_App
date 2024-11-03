from sqlalchemy import Column, Integer, String

from classes.policy.input import *

class ContactMixin:
    email         = Column(String(255), nullable=True, info={'Policy':EmailPolicy})
    mobile_number = Column(String(14), nullable=True, info={'Policy':MobilePolicy})
    extension     = Column(Integer, nullable=True, info={'Policy':EnsureInteger})