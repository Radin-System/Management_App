import hashlib

class StringTool:
    ## str to str
    @staticmethod
    def Strip(String:str) -> str:
        return String.strip()

    @staticmethod
    def Lower(String:str) -> str:
        return String.lower()

    @staticmethod
    def MD5(Raw:str) -> str:
        Md5 = hashlib.md5()
        Md5.update(Raw.encode())
        return Md5.hexdigest()

    @staticmethod
    def Sha224(Raw:str) -> str:
        Sha = hashlib.sha224()
        Sha.update(Raw.encode())
        return Sha.hexdigest

    @staticmethod
    def Sha256(Raw:str) -> str:
        Sha = hashlib.sha256()
        Sha.update(Raw.encode())
        return Sha.hexdigest()

    @staticmethod
    def Sha384(Raw:str) -> str:
        Sha = hashlib.sha384()
        Sha.update(Raw.encode())
        return Sha.hexdigest

    @staticmethod
    def Sha512(Raw:str) -> str:
        Sha = hashlib.sha512()
        Sha.update(Raw.encode())
        return Sha.hexdigest()

    ## str to int
    def GetInt(String:str) -> int:
        return int(String)

    ## str to float
    def GetFloat(String:str) -> float:
        return float(String)

    ## str to int or float
    @staticmethod
    def GetNumber(String:str) -> str | int | float:
        if String.isdigit():
            return int(String)

        return float(String)

    ## str to bool or None
    @staticmethod
    def GetBool(String:str) -> bool | None:
        if String.lower() in ['true','yes'] :
            return True

        elif String.lower() in ['false','no']:
            return False

        elif String.lower() in ['none','null','']:
            return None

        raise ValueError(f'Provided string do not match to any bool conditions: {String}')

    ## str to list
    @staticmethod
    def Split(String:str) -> list:
        return [Item.strip() for Item in String.split()]

    @staticmethod        
    def CsvToList(CSV:str) -> list:
        return [Item.strip() for Item in CSV.split(',')]