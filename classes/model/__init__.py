from .tables.user import User
from .tables.contact import Contact
from .tables.contact_book import Contact_Book

from ._base import Base

Models = [
    User,
    Contact,
    Contact_Book,
    ]

__all__ = [
    'Models',
    'Base',
]