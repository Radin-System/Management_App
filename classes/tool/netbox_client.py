from typing import Any, Dict
from netbox_python import NetBoxClient
from netbox_python import Result as _

class NetboxClient(NetBoxClient):

    def __init__(self, Base_URL: str, Token: str, Headers: Dict[str, str] = None):
        super().__init__(Base_URL, Token, Headers)