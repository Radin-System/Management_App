import hashlib
from typing import Any
from cryptography.fernet import Fernet

def CleanStr(String:Any) -> str:
    return str(String).strip()

def LowerCase(String:Any) -> str:
    return str(String).lower()

def CsvToList(CSV:str) -> list:
    return [Item.strip() for Item in CSV.split(',')]

def StrToMD5(Raw:str) -> str:
    MD5 = hashlib.md5()
    MD5.update(Raw.encode())
    return MD5.hexdigest()

def StrToSha(Raw:str) -> str:
    Sha = hashlib.sha256()
    Sha.update(Raw.encode())
    return Sha.hexdigest()

def Encrypt(Phrase:str, Key:bytes, Encoding='utf-8') -> bytes:
    frenet = Fernet(Key)
    return frenet.encrypt(Phrase.encode(Encoding))

def Decrypt(Token:bytes, Key:bytes, Encoding='utf-8') -> str:
    frenet = Fernet(Key)
    return frenet.decrypt(Token).decode(Encoding)

__all__ = [
    'CleanStr',
    'LowerCase',
    'CsvToList',
    'StrToMD5',
    'StrToSha',
    'Encrypt',
    'Decrypt',
]