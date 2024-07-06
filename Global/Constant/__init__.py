import os
from Global.Class import Config

ROOT       = os.getcwd()
CONFIGFILE = '.configfiles/server.ini'

Config_Manager = Config(CONFIGFILE)