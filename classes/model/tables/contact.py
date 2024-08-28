from sqlalchemy import  Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from classes.model.mixins import *
from classes.model.column_info import *

class Contact(BaseMixin, InfoMixin, NameMixin, OwnerMixin):
    __tablename__ = 'contacts'
    number = Column(String(50), nullable=False, info={'Policy':CleanString})

    # Foreign key to reference the contact_books table
    contact_book_id = Column(Integer, ForeignKey('contact_books.id'), nullable=False)

    # Define the relationship
    contact_book = relationship('Contact_Book', back_populates='contacts')