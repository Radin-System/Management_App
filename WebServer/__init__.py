from .Class               import FlaskWebServer
from .Blueprint           import Blueprints
from Global.Constant      import WEBSERVER_BIND_IP , WEBSERVER_BIND_PORT
from Global.Class.Network import IPv4 , Port

WebServer = FlaskWebServer(
    Host = IPv4(WEBSERVER_BIND_IP) ,
    Port = Port(WEBSERVER_BIND_PORT) ,
    )
WebServer.Name = 'WebServer'
WebServer.Init_Blueprints(Blueprints)