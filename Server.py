from flask import Flask

CONFIGFILE = '.configfiles/config.ini'

if __name__ == '__main__' :
    from classes.console import Console
    from classes.component import *
    from classes.model import *
    from blueprints import Blueprints

    MainConsole = Console(
        Startup=['reassign_dependencies', 'start_all'],
        Shutdown=['stop_all'],
        )

    Main_Config = Config('MainConfig', Config_File=CONFIGFILE)

    Main_Logger = Logger('MainLogger')

    Main_SQLManager = SQLManager('MainSQLManager',
        Base = Base,
        Models = Models,
        )

    Main_Webserver = WebServer('MainWebServer', 
        App = Flask(__name__, static_folder='static', template_folder='templates'),
        Blueprints = Blueprints,
        )

    MainConsole.Start()