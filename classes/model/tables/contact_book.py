from sqlalchemy import  Column, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.model.column_info import *

class Contact_Book(BaseMixin, InfoMixin, OwnerMixin):
    __tablename__ = 'contact_books'
    name = Column(String(50), nullable=False, unique=True, info={'Policy':NamePolicy_En})

    contacts = relationship('Contact', back_populates='contact_book', cascade='all, delete-orphan')
