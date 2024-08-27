class Tool :
    Logger = print

    def __str__(self) -> str :
        return f'<Tool :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'