from .api import Api
from .auth import Auth
from .error import Error
from .faq import Faq
from .root import Root
from .user import User

Blueprints = [
    Api,
    Auth,
    #Error,
    Faq,
    Root,
    User,
]

__all__ = []