from .api import Api
from .auth import Auth
from .error import Error
from .faq import Faq
from .register import Register
from .root import Root

Blueprints = [
    Api,
    Auth,
    Error,
    Faq,
    Register,
    Root,
]

__all__ = []