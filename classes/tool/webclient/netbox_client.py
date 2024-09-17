from typing import Any, Dict
from netbox_python import NetBoxClient
from netbox_python import Result as _

from classes.abstract.crud import CRUD
from ._base import WebClient

class NetboxClient(NetBoxClient, CRUD, WebClient):

    def __init__(self, Base_URL: str, Token: str, Headers: Dict[str, str] = None):
        super().__init__(Base_URL, Token, Headers)