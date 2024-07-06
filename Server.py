if __name__ == '__main__' :
## Prepair
    import sys
    from Global.Class.Logger import Logger

## Componnets
    from SQLManager   import SQLManager
    from AMIManager   import AMIManager

    Components = [
    SQLManager ,
    AMIManager ,
]

## Runtime
    try :
        for Component in Components : Component.Start()
    except Exception as e :
        for Component in Components        : Component.Stop()
        for Instance  in Logger._Instances : Instance.Stop()
        sys.exit(1)

## Exiting
    for Component in Components        : Component.Stop()
    for Instance  in Logger._Instances : Instance.Stop()
    sys.exit(0)