import os
from datetime import datetime
from ._base import Component

class Logger(Component):
    def __init__(self,*,
            Log_File:str,
            Debug_Condition:bool,
            Header:str,
            Time_Format:str,
            ) -> None :

        self.Log_File    = Log_File
        self.Condition   = Debug_Condition
        self.Header      = Header
        self.Time_Format = Time_Format

        self.Check_Folder()

    def Check_Folder(self) -> None :
        try :
            if  not os.path.exists(self.Log_File) :
                os.mkdir(os.path.dirname(self.Log_File))
                self(f'Created The Log Folder and File : {self.Log_File}')
        except FileExistsError : pass

    def __call__(self, Text:str, Formated = True) -> None :
        Time = datetime.now()
        LogText = f'{self.Header[0]} {Time.strftime(self.Time_Format)} : {Text} {self.Header[1]}'.replace('\n','')+'\n' if Formated else Text
        with open(self.Log_File , mode = 'a') as File : File.write(LogText)
        if self.Condition : print(LogText , end='')
    
    def Start_Actions(self) -> None:
        pass

    def Stop_Actions(self) -> None:
        pass