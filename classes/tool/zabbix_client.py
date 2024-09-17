from ._base import Tool
from zabbix_utils import ZabbixAPI

class ZabbixClient(ZabbixAPI, Tool):
    def __init__(self, Base_Url:str|None=None, Token:str|None = None,*,
        User:str|None=None, 
        Password:str|None=None,
        http_user:str|None=None, 
        http_password:str|None=None, 
        skip_version_check:bool=False, 
        validate_certs:bool=True, 
        timeout:int=30
        ) -> None:
        super().__init__(Base_Url, Token, User, Password, http_user, http_password, skip_version_check, validate_certs, timeout)