def Hello(Session) :
    Action = {
        'Action' : 'Hello' ,
        'Message' : 'Hello Server !'
        }
    Response = Session.Send(Action)
    return Response.Dict.get('Response')

def Ping(Session) :
    import time
    Action = {
        'Action'    : 'Ping' ,
        'Start_Time' : str(time.time()) ,
        }
    Response = Session.Send(Action)
    return Action.get('Start_Time') , Response.Dict.get('End_Time',None)
    
def Version(Session) :
    Action = {
        'Action' : 'Version' ,
        }
    Response = Session.Send(Action)
    return Response.Dict.get('Response')


def Disconnect(Session) :
    Action = {
        'Action' : 'Disconnect'
        }
    Response = Session.Send(Action)
    return Response.Dict.get('Response')