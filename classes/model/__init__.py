from .table.user import User
from .table.contact import Contact
from .table.contact_book import Contact_Book

from ._base import Base

Models:dict = {
    'User':User,
    'Contact':Contact,
    'Contact_Book':Contact_Book,
    }

__all__ = [
    'Models',
    'Base',
]