import time
from flask import Flask

CONFIGFILE = '.configfiles/config.ini'

if __name__ == '__main__' :
    from classes.console import Console
    from classes.component import *
    from classes.model import *
    from blueprints import Blueprints

    MainConsole = Console()

    Main_Config = Config('MainConfig', Config_File=CONFIGFILE)

    Main_Logger = Logger('MainLogger')

    Main_SQLManager = SQLManager('MainSQLManager', Base=Base, Models=Models)

    Main_Webserver = WebServer('MainWebServer', Blueprints=Blueprints)

    Main_Logger('Reassinging Dependencies')
    ComponentContainer.Reassign_Dependencies()

    Main_Logger('Starting all Components')
    ComponentContainer.Start_All()

    time.sleep(2)
    MainConsole.Start()

    Main_Logger('Stopping all Components')
    ComponentContainer.Stop_All()