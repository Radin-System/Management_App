from datetime        import datetime
from Global.Constant import DEBUG , LOG_TIME_FORMAT , LOG_HEADER , COLOUR_MAP

class Logger :
    _Instances = []

    def __init__(self , Name : str , LogFile : str , Debug_Condition : bool) -> None :
        self.Name      = Name
        self.Condition = Debug_Condition
        self.LogFile   = LogFile
        self.Active    = False
        self.Start()
        Logger._Instances.append(self)

    def Start(self) -> None :
        if not self.Active :
            self.Active = True

    def Stop(self) -> None :
        if self.Active :
            self.Active = False

    def Log(self , Text : str) -> None :
        self(Text , Colour = 'log')

    def Info(self , Text : str) -> None : 
        self(Text , Colour = 'information')

    def Warning(self , Text : str) -> None :
        self(Text , Colour = 'warning')

    def Error(self , Text  : str , Code : int) -> None :
        self(f'{Text} ErrorCode:{str(Code)}' , Colour = 'error')

    def Critical(self , Text : str) -> None :
        self(Text , Colour = 'critical')

    def __call__(self , Text : str , Colour = '' , Formated = True) -> None :
        if self.Active :
            Time = datetime.now()
            LogText = f'{LOG_HEADER[0]} {Time.strftime(LOG_TIME_FORMAT)} - {self.Name} : {Text} {LOG_HEADER[1]}'.replace('\n','')+'\n' if Formated else Text
            with open(self.LogFile , mode = 'a') as File : File.write(LogText)
            if self.Condition or DEBUG : 
                Colour_Code = COLOUR_MAP.get(Colour.lower(),'')
                print(f'{Colour_Code}{LogText}\033[0m' if Colour_Code else LogText , end='')

    def __str__(self) -> str :
        return f"<{self.Name} - Debug : {'On' if self.Condition else 'Off'}>"

    def __bool__(self) -> bool :
        return self.Active