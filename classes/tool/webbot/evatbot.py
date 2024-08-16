from selenium.webdriver.common.by import By
from Class.tool.imagereader import ImageReader
from . import WebBot


class EvatBot(WebBot):
    def __init__(self, Driver_Path:str, Base_URL:str, ImageReader:ImageReader) -> None:
        super().__init__(Driver_Path, Base_URL)

        self.ImageReader = ImageReader

    def Handel_Math_Text(self, Image_Path:str) -> int:
        Tries = 0
        while Tries < 5:
            Tries += 1
            self.Sleep(1)
            Captcha = self.Driver.find_element(By.ID,'capimg2')
            Refresh_Button = self.Driver.find_element(By.ID,'RefreshImg')

            self.Remove_CSS(Captcha)

            Captcha.screenshot(Image_Path)
            Text = self.ImageReader.Extract_Text(Image_Path).strip()
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

    def Get_From_Legal_ID(self,Legal_ID:int) -> dict:
        self.Get('frmNewvalidationofregistration.aspx')
        self.Fill_Input(By.ID,'LegalNatIDNo',Legal_ID)
        self.Fill_Input(By.ID,'CaptchaText',self.Handel_Math_Text('.temp/capimg2.png'))
        self.Sleep()
        Button = self.Driver.find_element(By.ID,'btnSearch2')
        Button.click()
