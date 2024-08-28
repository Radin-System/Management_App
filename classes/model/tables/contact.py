from sqlalchemy import  Column, String

from classes.model.mixins import *
from classes.model.column_info import *

class Contact(BaseMixin, InfoMixin, NameMixin, OwnerMixin):
    __tablename__ = 'contacts'
    number = Column(String(50), nullable=False, info={'Policy':CleanString})