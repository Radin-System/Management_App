import os
from Global.Class import Config

ROOT       = os.getcwd()
CONFIGFILE = '.configfiles/config.ini'

Config_Manager = Config(CONFIGFILE)