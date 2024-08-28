from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Dict[str, Any]] = {
    'ENVIRON' : {
        'crypto_key': 'qU-6rPX00wrsGYbmm3ts5Yhu_kByuaAAmD88mmNNhrA=',  # Test Key
        },

    'GLOBALS' : {
        'debug': True,
        'development_mode':True,
        'log_file': '.log/main.txt',
        'name': 'RSTO',
        'version': '1.1b',
        'language': 'fa',
        'temp_foldes_csv':'.temp,.error,',
        'develop_files_csv':'.temp,.log,.db,.error,',
        },

    'LOG' : {
        'log_time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
        'log_header': '<>',
        'log_max_size': '10MB'
        },

    'SQLMANAGER' : {
        'debug': True,
        'mode': 'SQLITE3',
        'host': '',
        'port': 0,
        'username': '',
        'password': '',
        'database': 'management_app',
        'sqlite_path': '.db/',
        'verbose': False,
        },

    'AMIMANAGER' : {
        'debug': False,
        'host': '',
        'port': 0,
        'tls_mode': False,
        'username': '',
        'password': '',
        'timeout': 10,
        'event_whitelist_csv': 'AgentConnect,AgentComplete',
        'max_action_id': 4096,
        },

    'WEBSERVER' : {
        'host': '0.0.0.0',
        'port': 8080,
        'Secret_Key': 'SDy9r3gbFDBjq0urv1398t0gsbuq0',
        },

    'WEBPAGESETTINGS' : {
        'dir': 'rtl',
        'main': True,
        'jquery': True,
        'charset': 'UTF-8',
        'appname': 'support_portal',
        'language': 'fa',
        'pagetitle': 'Support Portal',
        'bootstrap': True,
        'fontAwesome': True,
        'fontvazirmtn': True,
        },

    'TOOL' : {
        'chrome_driver_path':'C:\\Program Files\\Google\\Chrome\\chromedriver.exe',
        'teseract_path': 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
        'sarv_url': 'https://app.sarvcrm.com/',
        'sarv_username': '',
        'sarv_password': '',
        'evat_url': 'https://evat.ir/',
        },
    }