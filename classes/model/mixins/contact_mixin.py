from sqlalchemy import Column, Integer, String

from classes.policy.input import *

class ContactMixin:
    email         = Column(String, nullable=True, info={'Policy':EmailPolicy})
    extension     = Column(Integer, nullable=True, info={'Policy':EnsureInteger})
    mobile_number = Column(String, nullable=True, info={'Policy':MobilePolicy})
