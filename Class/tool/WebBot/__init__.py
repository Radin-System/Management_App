import time,random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from Class.tool import Tool

class WebBot(Tool):
    def __init__(self,Driver_Path:str,Base_URL) -> None:
        self.Driver_Path = Driver_Path
        self.Base_URL = Base_URL

        self.Driver = webdriver.Chrome(service=Service(self.Driver_Path))
        self.Wait = WebDriverWait(self.Driver, 10)

    def Get(self,URL) -> None :
        self.Driver.get(self.Base_URL+URL)
        self.Wait.until(EC.visibility_of_all_elements_located)

    def Sleep(self,Seconds:int) -> None :
        time.sleep(Seconds + random.uniform(0,2))

    def Fill_Input(self,by:By, identifier:str, text:str , clear=True) -> WebElement:
        Input = self.Driver.find_element(by,identifier)
        if clear : Input.clear()
        Input.send_keys(text)
        return Input

    def Click_Element(self,by:By, identifier:str) -> WebElement:
        Element = self.Driver.find_element(by,identifier)
        Element.click()
        return Element

    def Remove_CSS(self,Element:WebElement) -> None:
        self.Driver.execute_script("var element = arguments[0];element.style.cssText = '';",Element)

    def Stop(self):
        self.Driver.quit()