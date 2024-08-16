import os
from typing           import Dict,Any
from configparser     import ConfigParser
from functions.convert import CsvToList

class Config:
    DEFAULT: Dict[str, Dict[str, Any]] = {}

    DEFAULT['ENVIRON'] = {
        'crypto_key': 'qU-6rPX00wrsGYbmm3ts5Yhu_kByuaAAmD88mmNNhrA='  # Test Key
    }

    DEFAULT['GLOBALS'] = {
        'debug': True,
        'development_mode':True,
        'log_file': '.log/main.txt',
        'name': 'RSTO',
        'version': '1.1b',
        'language': 'fa',
        'temp_foldes_csv':'.temp,.error,',
        'develop_files_csv':'.temp,.log,.db,.error,',
    }

    DEFAULT['LOG'] = {
        'log_time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
        'log_header': '<>',
        'log_max_size': '10MB'
    }

    DEFAULT['TASKMANAGER'] ={
        'check_interval': 5,
    }

    DEFAULT['SQLMANAGER'] = {
        'debug': True,
        'mode': 'SQLITE3',
        'host': '',
        'port': 0,
        'username': '',
        'password': '',
        'database': 'management_app',
        'sqlite_path': '.db/',
        'verbose': False,
    }

    DEFAULT['AMIMANAGER'] = {
        'debug': False,
        'host': '',
        'port': 0,
        'tls_mode': False,
        'username': '',
        'password': '',
        'timeout': 10,
        'event_whitelist_csv': 'AgentConnect,AgentComplete',
        'max_action_id': 4096,
    }

    DEFAULT['WEBSERVER'] = {
        'host': '0.0.0.0',
        'port': 8080,
        'flask_debug': True,
        'Secret_Key': 'SDy9r3gbFDBjq0urv1398t0gsbuq0',
    }

    DEFAULT['TOOL'] = {
        'chrome_driver_path':'C:\\Program Files\\Google\\Chrome\\chromedriver.exe',
        'teseract_path': 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
        'sarv_url': 'https://app.sarvcrm.com/' ,
        'sarv_username': '',
        'sarv_password': '',
        'evat_url': 'https://evat.ir/',
    }

    def __init__(self, Config_File:str) -> None:
        self.Config_File = Config_File
        self.Config = ConfigParser()
        self.Load()
        for K,V in self.Config['ENVIRON'].items(): os.environ.setdefault(K,str(V))

    def Load(self) -> None:
        ## Cheking if file exist
        if os.path.exists(self.Config_File):
            self.Config.read(self.Config_File)
            Updated = False
            ## Cheking if all the sections exists in the config file
            for Section, Params in self.DEFAULT.items():
                if not self.Config.has_section(Section):
                    self.Config.add_section(Section)
                    Updated = True
                for Key, Value in Params.items():
                    if not self.Config.has_option(Section, Key):
                        self.Config.set(Section, Key, str(Value))
                        Updated = True

            ## Updates file if any section or parameter is added
            if Updated: self.Save()

        ## Creates new file if file is missing
        else: 
            for Section, Parameters in self.DEFAULT.items():
                Parameters = {K:str(V) for K,V in Parameters.items()}
                self.Config[Section] = Parameters

            self.Save()

    def Get(self,Sec:str,Parm:str,*,
            Fallback:Any=None, 
            Raise_On_Missing:bool=True
            ) -> Any:

        if Raise_On_Missing:
            if not self.Config.has_section(Sec): raise KeyError(f'Provided config file does not have this section :{Sec}')
            if not self.Config.has_option(Sec, Parm): raise KeyError(f'Provided config file does not have this parameter :{Sec}-{Parm}')

        Value = self.Config.get(Sec, Parm)

        if Parm.endswith('_csv') : return CsvToList(Value)

        if   Value.lower() in ['none','null','']: return Fallback
        elif Value.lower() in ['true','yes']: return True
        elif Value.lower() in ['false','no']: return False
        elif Value.isdigit(): return int(Value)
        else: return Value

    def Set(self, Section, Parameter, Value) -> None:
        self.Config.set(Section, Parameter, str(Value))
        self.Save()
    
    def Save(self) -> None:
        with open(self.Config_File, 'w') as Config_File:
            self.Config.write(Config_File)