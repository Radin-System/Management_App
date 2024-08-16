from .api import Api
from .auth import Auth
from .error import Error
from .faq import Faq
from .root import Root

Blueprints = [
    Api,
    Auth,
    #Error,
    Faq,
    Root,
]

__all__ = []