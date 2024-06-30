import os
from datetime        import datetime
from Global.Constant import DEBUG , LOG_PATH , LOG_TIME_FORMAT , LOG_HEADER

class Logger :
    _Instances = []

    def __init__(self , Name : str , LogFile : str , Debug_Condition : bool) -> None :
        self.Name      = Name
        self.Condition = Debug_Condition
        self.LogFile   = LogFile
        self.Active    = False
        self.Check_Folder()
        self.Start()
        Logger._Instances.append(self)

    def Check_Folder(self) -> None :
        try : os.mkdir(LOG_PATH) if not os.path.exists(os.path.join(LOG_PATH,self.LogFile)) else ...
        except FileExistsError : pass

    def Start(self) -> None :
        if not self.Active :
            self.Active = True

    def Stop(self) -> None :
        if self.Active :
            self.Active = False

    def Log(self, Text:str) -> None :
        self(Text, Colour = 'log')

    def __call__(self, Text : str , Colour = '' , Formated = True) -> None :
        if self.Active :
            Time = datetime.now()
            LogText = f'{LOG_HEADER[0]} {Time.strftime(LOG_TIME_FORMAT)} - {self.Name} : {Text} {LOG_HEADER[1]}'.replace('\n','')+'\n' if Formated else Text
            with open(os.path.join (LOG_PATH,self.LogFile) , mode = 'a') as File : File.write(LogText)
            if self.Condition or DEBUG :
                print(LogText , end='')

    def __str__(self) -> str :
        return f"<{self.Name} - Debug : {'On' if self.Condition else 'Off'}>"

    def __bool__(self) -> bool :
        return self.Active