if __name__ == '__main__' :
## Prepair
    import sys

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
        sys.exit(1)

## Exiting
    for Component in Components        : Component.Stop()
    sys.exit(0)