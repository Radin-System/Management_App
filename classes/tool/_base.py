class Tool :
    def __init__(self,Name) -> None:
        from classes.tool import ToolContainer

        self.Name = Name
        ToolContainer.Register(Name, self)

    def Init_Dependancy(self) -> None:
        from classes.tool import ToolContainer
        from classes.tool import Logger
        from classes.tool import Config

        self.Logger:Logger = ToolContainer.Get(f'{self.Name}_Logger', ToolContainer.Get('Main_Logger', print))
        self.Config:Config = ToolContainer.Get(f'{self.Name}_Config', ToolContainer.Get('Main_Config'))

    def Init_Config(self) -> None:
        raise NotImplementedError(f'Please provide an action for configuring the component: {self.Name}')

    def __str__(self) -> str :
        return f'<Tool :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'
