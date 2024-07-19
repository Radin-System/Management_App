from selenium.webdriver.common.by import By
from Class.tool.imagereader import ImageReader
from . import WebBot


class Evat_Bot(WebBot):
    def __init__(self, Driver_Path:str, Base_URL:str, ImageReader:ImageReader) -> None:
        super().__init__(Driver_Path, Base_URL)

        self.ImageReader = ImageReader

    def Handel_Math_Text(self, Image_Path:str) -> int :
        Tries = 0
        while Tries < 5:
            Tries += 1
            self.Sleep(1)
            Captcha = self.Driver.find_element(By.ID,'capimg2')
            Refresh_Button = self.Driver.find_element(By.ID,'RefreshImg')

            self.Driver.execute_script("var element = arguments[0];element.style.cssText = '';",Captcha)

            Captcha.screenshot(Image_Path)
            Text = self.ImageReader.Extract_Text(Image_Path).replace('i','1').strip()
            print(f'Captcha Text :[{Text}]')

            if '+' in Text :
                try: 
                    Math_Sections = Text.split('+')
                    x,y = int(Math_Sections[0].strip()),int(Math_Sections[1].strip())
                    Result = x + y
                    return int(Result)
                except : pass
            
            Refresh_Button.click()
        else: raise TimeoutError(f'Unable to get capcha in {Tries} tries')

    def Get_From_LegalID(self,ID:int) -> dict :
        self.Get('frmNewvalidationofregistration.aspx')
        self.Fill_Input(By.ID,'LegalNatIDNo',ID)
        self.Fill_Input(By.ID,'CaptchaText',self.Handel_Math_Text('capimg2.png'))
        self.Sleep(1)
        Button = self.Driver.find_element(By.ID,'btnSearch2')
        Button.click()
        self.Sleep(20)