import platform
from pytesseract import pytesseract
from PIL import Image as img

class ImageReader:
    def __init__(self,Tesseract_Path:str = None) -> None :
        self.Tesseract_Path = Tesseract_Path
        if platform.system().lower() == 'windows' :
            pytesseract.tesseract_cmd = self.Tesseract_Path
        else :
            print('Make Sure implement teseract with Homebrew')
    
    def Extract_Text (self,Image_Path:str) -> str :
        Image = img.open(Image_Path)
        Text = pytesseract.image_to_string(Image,lang='eng')
        return Text