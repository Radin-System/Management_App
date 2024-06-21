from .Class          import AsteriskAMIManager
from Global.Constant import AMIMANAGER_HOST , AMIMANAGER_PORT , AMIMANAGER_USERNAME , AMIMANAGER_PASSWORD

AMIManager = AsteriskAMIManager(
                                Host     = AMIMANAGER_HOST , 
                                Port     = AMIMANAGER_PORT , 
                                Username = AMIMANAGER_USERNAME , 
                                Secret   = AMIMANAGER_PASSWORD ,
                                )
AMIManager.Name = 'AMIManager'