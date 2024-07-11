from . import Validate
from Class.constants import CIDR_MAP, MASK_MAP

class Convert :

    @staticmethod
    def CSVToList(CSV:str) -> list :
        return [Item.strip() for Item in CSV.split(',')]

    @staticmethod
    def MaskToCIDR(Mask : str) -> str :
        if Validate.Mask(Mask) :
           return CIDR_MAP.get(Mask , '')
        return ''

    @staticmethod
    def CIDRToMask(CIDR : str) -> str :
        if Validate.CIDR(CIDR) :
            return MASK_MAP.get(CIDR , '')
        return ''
