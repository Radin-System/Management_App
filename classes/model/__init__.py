from .tables.authentication import Authentication
from .tables.company import Company
#from .tables.device import Device
from .tables.location import Location
from .tables.node import Node
from .tables.personnel import Personnel
from .tables.user import User
from .base import Base

Models = [
    Authentication,
    Company,
#    Device,
    Location,
    Node,
    Personnel,
    User,
    ]

__all__ = [
    'Models',
    'Base',
]