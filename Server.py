if __name__ == '__main__' :
## Prepair
    import sys
    from Global.Constant     import GlobalManager
    from Global.Class.Logger import Logger

## Componnets
    from WebServer    import WebServer
    from SQLManager   import SQLManager
    from AMIManager   import AMIManager

    Components = [
    SQLManager ,
    WebServer ,
    AMIManager ,
]

## Runtime
    GlobalManager.Logger('Application Started')
    try :
        GlobalManager.Logger('Starting Application Components')
        for Component in Components : Component.Start()
    except Exception as e :
        GlobalManager.Logger(f'Faild to Start {Component.Name} Becuse : {e}')
        for Component in Components        : Component.Stop()
        for Instance  in Logger._Instances : Instance.Stop()
        sys.exit(1)

## Exiting
    GlobalManager.Logger('Stopping Application Componnets')
    for Component in Components        : Component.Stop()
    GlobalManager.Logger('Application Shutdown')
    GlobalManager.Logger('Closing Logging')
    for Instance  in Logger._Instances : Instance.Stop()
    sys.exit(0)