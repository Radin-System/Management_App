import os,json
from typing import Dict,Any
from configparser import ConfigParser
from Global.Function import Convert
from datetime        import datetime

class Empty :
    def __init__(self) -> None:
        pass

class Config:
    DEFAULT: Dict[str, Dict[str, Any]] = {}

    DEFAULT['ENVIRON'] = {
        'crypto_key': 'qU-6rPX00wrsGYbmm3ts5Yhu_kByuaAAmD88mmNNhrA='  # Test Key
        }
    
    DEFAULT['GLOBALS'] = {
        'debug': True,
        'log_path': '.Log/',
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
        'task_timeout': 365
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
        'username': None,
        'password': None,
        'database': 'management_app',
        'sqlite_path': '.db/',
        'verbose': False,
        }
    
    DEFAULT['AMIMANAGER'] = {
        'debug': False,
        'host': '127.0.0.1',
        'port': 5038,
        'tls_mode': False,
        'username': None,
        'password': None,
        'timeout': 10,
        'max_actionid': 2048,
        'event_whitelist_csv': 'AgentConnect,AgentComplete',
        }

    def __init__(self, Config_File : str) -> None:
        self.Config_File = Config_File
        self.Config = ConfigParser()
        self.Load_Config()

    def Load_Config(self) -> None:
        Config_Dir = os.path.dirname(self.Config_File)
        if Config_Dir and not os.path.exists(Config_Dir) : os.makedirs(Config_Dir)
        if os.path.exists(self.Config_File):
            self.Config.read(self.Config_File)
            self.Check_Config()
        else: self.Init_Default()

    def Init_Default(self) -> None:
        for Section, Params in self.DEFAULT.items():
            Params = {K:str(V) for K,V in Params.items()}
            self.Config[Section] = Params
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

    def Get(self, Section:str, Key:Any, Fallback:Any=None) -> None:
        if not self.Config.has_option(Section, Key): return Fallback
        
        Value = self.Config.get(Section,Key)
        
        if Value.lower() in ['none','null'] : return None
        if Value.lower() in ['true','yes']  : return True
        if Value.lower() in ['false','no']  : return False

        try: return int(Value)
        except ValueError:
            if Section.endswith('_csv') :
                try: return Convert.CSVToList(Value)
                except json.JSONDecodeError: return Value
            else : return Value
            
    def Set(self, Section, Key, Value) -> None:
        if not self.Config.has_section(Section) : self.Config.add_section(Section)
        self.Config.set(Section, Key, str(Value))
        self.Save_Config()

class Logger :
    def __init__(self,*,
                 Name:str,
                 LogFile:str,
                 Debug_Condition:bool,
                 Header:str,
                 Time_Format:str,) -> None :
        self.Name        = Name
        self.LogFile     = LogFile
        self.Condition   = Debug_Condition
        self.Header      = Header
        self.Time_Format = Time_Format

        self.Active      = False

        self.Check_Folder()
        self.Start()

    def Check_Folder(self) -> None :
        os.mkdir(os.path.dirname(self.LogFile)) if not os.path.exists(self.LogFile) else ...

    def Start(self) -> None :
        if not self.Active :
            self.Active = True

    def Stop(self) -> None :
        if self.Active :
            self.Active = False

    def Log(self, Text:str) -> None :
        self(Text, Colour = 'log')

    def __call__(self, Text : str , Colour = '' , Formated = True) -> None :
        if self.Active :
            Time = datetime.now()
            LogText = f'{self.Header[0]} {Time.strftime(self.Time_Format)} - {self.Name} : {Text} {self.Header[1]}'.replace('\n','')+'\n' if Formated else Text
            with open(self.LogFile , mode = 'a') as File : File.write(LogText)
            if self.Condition :
                print(LogText , end='')

    def __str__(self) -> str :
        return f"<{self.Name} - Debug : {'On' if self.Condition else 'Off'}>"

    def __bool__(self) -> bool :
        return self.Active

class Component :
    def __init__(self) -> None:
        self.Name : str = 'Empty Component'
        self.Running : bool = None

    def Start_Actions(self) -> None :
        raise NotImplementedError('Please provide a Action for starting the componnet')

    def Stop_Actions(self) -> None:
        raise NotImplementedError('Please provide a Action for stopping the componnet')

    def Start(self) -> None:
        if not self.Running :
            self.Running = True
            self.Start_Actions()

    def Stop(self) -> None:
        if self.Running :
            self.Running = False
            self.Stop_Actions()

    def __bool__(self) -> bool :
        return self.Running

    def __str__(self) -> str :
        return f'<Component :{self.Name}>'

    def __repr__(self) -> str:
        return ''