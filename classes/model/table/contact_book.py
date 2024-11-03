from sqlalchemy import  Column, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.policy.input import *

class Contact_Book(BaseMixin, IdMixin, FlagMixin, AuditMixin, OwnerMixin):
    __tablename__ = 'contact_books'
    name = Column(String(255), nullable=False, unique=True, info={'Policy':NamePolicy_En})

    contacts = relationship('Contact', back_populates='contact_book', cascade='all, delete-orphan')
