import os,shutil
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
        'temp_foldes_csv':'.temp,',
        'develop_files_csv':'.temp,.log,.db',
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
        'max_action_id': 2048,
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

    def __init__(self, Config_File : str) -> None:
        self.Config_File = Config_File
        self.Config = ConfigParser()
        self.Create_Ignored_Folders()
        self.Load_Config()
        self.Set_Enviroment()
        self.Check_Development_Mode()
        self.Remove_Temp_Folders()
        self.Create_Ignored_Folders()

    def Load_Config(self) -> None:
        if os.path.exists(self.Config_File):
            self.Config.read(self.Config_File)
            self.Check_Config()
        else: 
            self.Init_Default()

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
        if not self.Config.has_section: raise KeyError(f'Provided config file does not have this section :{Section}')
        if not self.Config.has_option(Section, Parameter): return Fallback

        Value = self.Config.get(Section,Parameter)

        if Parameter.endswith('_csv') : return CsvToList(Value)

        if   Value.lower() in ['none','null','']: return Fallback
        elif Value.lower() in ['true','yes']: return True
        elif Value.lower() in ['false','no']: return False
        elif Value.isdigit(): return int(Value)
        else: return Value

    def Set(self, Section, Parameter, Value) -> None:
        if not self.Config.has_section(Section) : self.Config.add_section(Section)
        self.Config.set(Section, Parameter, str(Value))
        self.Save_Config()

    def Create_Ignored_Folders(self) -> None:
        with open('.gitignore') as Ignored:
            for Line in Ignored.readlines() :
                Folder = Line.strip().replace('/','')
                if not os.path.exists(Folder) :
                    os.mkdir(Folder)

    def Check_Development_Mode(self) -> None:
        Development_Mode = self.Get('GLOBALS','development_mode',False)
        if Development_Mode :
            print('Warning, The application is running in Development mode, All logs,databases,configs will be recreated on next run')
            Folders = self.Get('GLOBALS','develop_files_csv',[])
            print('Removing following folders :',Folders)
            for Folder in Folders :
                if os.path.exists(Folder):
                    shutil.rmtree(Folder)
    
    def Remove_Temp_Folders(self) -> None:
        Folders = self.Get('GLOBALS','temp_foldes_csv',[])
        for Folder in Folders :
            if os.path.exists(Folder):
                shutil.rmtree(Folder)