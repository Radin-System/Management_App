from .tables.user import User
from ._base import Base

Models = [
    User,
    ]

class ModelsTyping:
    def __typing__(self) -> None:
        self.User = User

__all__ = [
    'Models',
    'Base',
]