from .tables.user import User
from .tables.contact import Contact

from ._base import Base

Models = [
    User,
    Contact,
    ]

__all__ = [
    'Models',
    'Base',
]