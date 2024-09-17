from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Dict[str, Any]] = {
    'ENVIRON' : {
        # Crypto
        'crypto_key': 'qU-6rPX00wrsGYbmm3ts5Yhu_kByuaAAmD88mmNNhrA=',  # Test Key
        },

    'GLOBALS' : {
        # General
        'debug': True,
        'log_file': '.log/main.txt',
        'name': 'RSTO',
        'version': '1.1b',
        'language': 'fa',
        },

    'LOG' : {
        # General
        'log_time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
        'log_header': '<>',
        'log_max_size': '10MB'
        },

    'SQLMANAGER' : {
        # General
        'debug': True,
        'mode': 'SQLITE3',
        'database': 'management_app',
        'sqlite_path': '.db/',
        'verbose': False,

        # Host
        'host': '',
        'port': 0,

        # Auth
        'username': '',
        'password': '',
        },

    'AMIMANAGER' : {
        # General
        'debug': False,
        'timeout': 10,
        'event_whitelist_csv': 'AgentConnect,AgentComplete',
        'max_action_id': 4096,

        # Host
        'host': '',
        'port': 0,

        # SSL
        'tls_mode': False,

        # Auth
        'username': '',
        'password': '',
        },

    'WEBSERVER' : {
        # Host
        'host': '0.0.0.0',
        'port': 8080,

        # Crypto
        'Secret_Key': 'SDy9r3gbFDBjq0urv1398t0gsbuq0',
        },

    'WEBPAGESETTINGS' : {
        # General
        'appname': 'support_portal',
        'pagetitle': 'Support Portal',
        'charset': 'UTF-8',
        'language': 'fa',
        'dir': 'rtl',

        # Static
        'bootstrap': True,
        'fontAwesome': True,
        'fontvazirmtn': True,
        'main': True,
        'jquery': True,
        },

    'TOOL' : {
        # WebDriver
        'chrome_driver_path':'C:\\Program Files\\Google\\Chrome\\chromedriver.exe',
        'teseract_path': 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',

        # URLs
        'evat_url': 'https://evat.ir/',
        'sarv_url': 'https://app.sarvcrm.com/',
        'netbox_url': None,
        'zabbix_url': None,

        # Auth
        'sarv_username': None,
        'sarv_password': None,

        # Token
        'netbox_token': None,
        'zabbix_token': None,
        },
    }