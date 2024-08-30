import os
from typing import Dict,Any
from configparser import ConfigParser

from classes.convert import StringTool
from constant import DEFAULT_CONFIG

from ._base import Component, ComponentContainer

class Config(Component):
    def __init__(self,Name:str,*,
            Config_File:str,
            ) -> None:

        super().__init__(Name)

        self.Process_Type: str = 'Static'

        self.Config_File = Config_File
        self.Parser = ConfigParser()
        self.Load()
        for K,V in self.Parser['ENVIRON'].items(): os.environ.setdefault(K,str(V))

    def Init_Config(self) -> None:
        ...

    def Init_Dependancy(self) -> None:
        self.Logger = ComponentContainer.Get('MainLogger', print)

    def Load(self) -> None:
        ## Cheking if file exist
        if os.path.exists(self.Config_File):
            self.Parser.read(self.Config_File)
            Updated = False
            ## Cheking if all the sections exists in the config file
            for Section, Params in DEFAULT_CONFIG.items():
                if not self.Parser.has_section(Section):
                    self.Parser.add_section(Section)
                    Updated = True
                for Key, Value in Params.items():
                    if not self.Parser.has_option(Section, Key):
                        self.Parser.set(Section, Key, str(Value))
                        Updated = True

            ## Updates file if any section or parameter is added
            if Updated: self.Save()

        ## Creates new file if file is missing
        else: 
            for Section, Parameters in DEFAULT_CONFIG.items():
                Parameters = {K:str(V) for K,V in Parameters.items()}
                self.Config[Section] = Parameters

            self.Save()

    def Get(self,Sec:str,Parm:str,*,
            Fallback:Any=None, 
            Raise_On_Missing:bool=True
            ) -> str | int | float | bool | list | None:

        if Raise_On_Missing:
            if not self.Parser.has_section(Sec): raise KeyError(f'Provided config file does not have this section :{Sec}')
            if not self.Parser.has_option(Sec, Parm): raise KeyError(f'Provided config file does not have this parameter :{Sec}-{Parm}')
        elif (not Raise_On_Missing) and (not self.Parser.has_section(Sec) or not self.Parser.has_option(Sec, Parm)):
            return None

        Value = self.Parser.get(Sec, Parm)

        # Return a list if Parm is CSV
        if Parm.endswith('_csv'): 
            return StringTool.CsvToList(Value)

        try:
            # Return int or float if is digit
            return StringTool.GetNumber(Value)
        except ValueError:
            try:
                # Returns bool if the value in (true,false,yes,no) if in (none,null) returns Fallback
                return Fallback if StringTool.GetBool(Value) is None else StringTool.GetBool(Value)
            except ValueError:
                pass

        # if None of the above conditions met returns str
        return Value

    def Set(self, Section, Parameter, Value) -> None:
        self.Parser.set(Section, Parameter, str(Value))
        self.Save()
    
    def Save(self) -> None:
        with open(self.Config_File, 'w') as Config_File:
            self.Parser.write(Config_File)
    
    def Start_Actions(self) -> None:
        ...
    
    def Stop_Actions(self) -> None:
        ...

    def Loop(self) -> None:
        ...