class Component :
    def __init__(self) -> None:
        self.Name : str = 'Empty Component'
        self.Running : bool = None

    def Start_Actions(self) -> None :
        raise NotImplementedError('Please provide an action for starting the componnet')

    def Stop_Actions(self) -> None:
        raise NotImplementedError('Please provide an action for stopping the componnet')

    def Start(self) -> None:
        if not self.Running :
            self.Running = True
            self.Start_Actions()

    def Stop(self) -> None:
        if self.Running :
            self.Running = False
            self.Stop_Actions()

    def __bool__(self) -> bool :
        return self.Running

    def __str__(self) -> str :
        return f'<Component :{self.Name}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.Name}",*Args,**Kwargs)'