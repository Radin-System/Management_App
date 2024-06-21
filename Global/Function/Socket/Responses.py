import time
from Global.Constant import VERSION

def Hello(Session,Message) :
    Response = {
        'ID'       : Message.Dict.get('ID') ,
        'Response' : 'Hello Client , Welcome to server !' ,
        }
    Session.Send(Response , 'Response')

def Ping(Session,Message) :
    Response = {
        'ID'       : Message.Dict.get('ID') ,
        'Response' : 'Pong' ,
        'End_Time' : str(time.time()) ,
        }
    Session.Send(Response , 'Response')
    
def Version(Session,Message) :
    Response = {
        'ID'       : Message.Dict.get('ID') ,
        'Response' : VERSION ,
        }
    Session.Send(Response , 'Response')
    
def Disconnect(Session,Message) :
    Response = {
        'ID'       : Message.Dict.get('ID') ,
        'Response' : 'GoodBye' ,
        }
    Session.Disconnect()
    Session.Send(Response , 'Response')