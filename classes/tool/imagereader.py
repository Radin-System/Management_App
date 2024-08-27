import platform
from pytesseract import pytesseract
from PIL import Image as img
from ._base import Tool

class ImageReader(Tool):
    def __init__(self,Tesseract_Path:str = None) -> None :
        self.Tesseract_Path = Tesseract_Path
        if platform.system() == 'Windows' :
            pytesseract.tesseract_cmd = self.Tesseract_Path
    
    def Extract_Text(self,Image_Path:str) -> str :
        Image = img.open(Image_Path)
        Text = pytesseract.image_to_string(Image,lang='eng')
        return Text