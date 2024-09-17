import time,random
from abc import abstractmethod
from typing import Self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from classes.tool._base import Tool

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

    @abstractmethod
    def Init_Config(self) -> None:
        ...

    def __str__(self) -> str :
        return f'<Tool :{self.__name__}>'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(*Args,**Kwargs)'

class WebBot(Tool):
    def __init__(self,Driver_Path:str,Base_URL) -> None:
        self.Driver_Path = Driver_Path
        self.Base_URL = Base_URL

        self.Driver = webdriver.Chrome(service=Service(self.Driver_Path))
        self.Wait = WebDriverWait(self.Driver, 10)

    def Get(self,URL) -> None :
        self.Driver.get(self.Base_URL+URL)
        self.Wait.until(EC.visibility_of_all_elements_located)

    def Sleep(self, Seconds:int=0) -> None :
        time.sleep(Seconds + random.uniform(0,2))

    def Fill_Input(self,by:By, Identifier:str, Text:str, Click:bool = False, Clear:bool = True) -> WebElement:
        Input = self.Driver.find_element(by,Identifier)
        if Clear : Input.clear()
        if Click : Input.click()
        Input.send_keys(Text)
        return Input

    def Click_Element(self,by:By, identifier:str) -> WebElement:
        Element = self.Driver.find_element(by,identifier)
        Element.click()
        return Element

    def Remove_CSS(self,Element:WebElement) -> None:
        self.Driver.execute_script("var element = arguments[0];element.style.cssText = '';",Element)

    def Stop(self):
        self.Driver.quit()
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self,Eexception_Type, Exception_Value, Traceback) -> None :
        self.Stop()