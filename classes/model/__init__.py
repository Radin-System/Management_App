from .tables.user import User
from ._base import Base

Models = [
    User,
    ]

__all__ = [
    'Models',
    'Base',
]