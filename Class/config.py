import os
from typing          import Dict,Any
from configparser    import ConfigParser
from . import Convert
from .Network import IPv4,Port
from .Auth import Username,Password

class Config:
    DEFAULT: Dict[str, Dict[str, Any]] = {}

    DEFAULT['ENVIRON'] = {
        'crypto_key': 'qU-6rPX00wrsGYbmm3ts5Yhu_kByuaAAmD88mmNNhrA='  # Test Key
        }

    DEFAULT['GLOBALS'] = {
        'debug': True,
        'log_file': '.log/main.txt',
        'name' : 'RSTO',
        'version' : '1.1b',
        'language': 'fa',
        }

    DEFAULT['LOG'] = {
        'log_time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
        'log_header': '<>',
        'log_max_size': '10MB'
        }

    DEFAULT['TASKMANAGER'] ={
        'chck_interval': 5,
        }

    DEFAULT['LDAPUSER'] = {
        'use_ssl': False,
        'validate_ssl': False,
        }

    DEFAULT['WEBSERVER'] = {
        'debug': False,
        'FLASK_DEBUG': False,
        'bind_ip': '127.0.0.1',
        'bind_port': 'HTTP',
        'tls_mode': False,
        'secret_key': 'd3u15q$w5if^uos*$775ig^njkf02421',  # Test Key
        'minify_html': True,
        }

    DEFAULT['SQLManager'] = {
        'debug': True,
        'mode': 'SQLITE3',
        'host': '127.0.0.1',
        'port': '0/ICMP',
        'username': 'admin', # Test Username
        'password': 'asd@123', # Test Password
        'database': 'management_app',
        'sqlite_path': '.db/',
        'verbose': False,
        }

    DEFAULT['AMIMANAGER'] = {
        'debug': False,
        'host': '127.0.0.1',
        'port': '5038/TCP',
        'tls_mode': False,
        'username': 'admin', # Test Username
        'password': 'asd@123', # Test Password
        'timeout': 10,
        'event_whitelist_csv': 'AgentConnect,AgentComplete',
        'max_action_id': 2048,
        }

    def __init__(self, Config_File : str) -> None:
        self.Config_File = Config_File
        self.Config = ConfigParser()
        self.Load_Config()
        self.Set_Enviroment()

    def Load_Config(self) -> None:
        Config_Dir = os.path.dirname(self.Config_File)
        if Config_Dir and not os.path.exists(Config_Dir) : os.makedirs(Config_Dir)
        if os.path.exists(self.Config_File):
            self.Config.read(self.Config_File)
            self.Check_Config()
        else: self.Init_Default()

    def Init_Default(self) -> None:
        for Section, Parameters in self.DEFAULT.items():
            Parameters = {K:str(V) for K,V in Parameters.items()}
            self.Config[Section] = Parameters
        self.Save_Config()

    def Check_Config(self) -> None :
        Updated = False
        for Section, Params in self.DEFAULT.items():
            if not self.Config.has_section(Section):
                self.Config.add_section(Section)
                Updated = True
            for Key, Value in Params.items():
                if not self.Config.has_option(Section, Key):
                    self.Config.set(Section, Key, str(Value))
                    Updated = True
        if Updated:
            self.Save_Config()

    def Save_Config(self) -> None:
        with open(self.Config_File, 'w') as Config_File:
            self.Config.write(Config_File)

    def Set_Enviroment(self) -> None:
        if self.Config.has_section('ENVIRON'):
            for K , V in self.Config['ENVIRON'].items(): os.environ.setdefault(K,str(V))

    def Get(self, Section:str, Parameter:str, Fallback:Any=None) -> Any:
        if not self.Config.has_section: raise KeyError('Provided config file does not have this section :',Section)
        if not self.Config.has_option(Section, Parameter): return Fallback

        Value = self.Config.get(Section,Parameter)

        if   Value.lower() in ['none','null'] : Value = None
        elif Value.lower() in ['true','yes']  : Value = True
        elif Value.lower() in ['false','no']  : Value = False
        elif Value.isdigit()                  : Value = int(Value)

        if   Parameter == 'host'        : return IPv4(Value)
        elif Parameter == 'port'        : return Port(Value)
        elif Parameter == 'username'    : return Username(Value)
        elif Parameter == 'password'    : return Password(Value)
        elif Parameter.endswith('_csv') : return Convert.CSVToList(Value)

        else : return Value

    def Set(self, Section, Parameter, Value) -> None:
        if not self.Config.has_section(Section) : self.Config.add_section(Section)
        self.Config.set(Section, Parameter, str(Value))
        self.Save_Config()