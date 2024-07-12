import os,hashlib
from cryptography.fernet import Fernet

class Crypto :

    @staticmethod
    def MD5 (Raw : str) -> str :
        MD5 = hashlib.md5()
        MD5.update(Raw.encode())
        return MD5.hexdigest()

    @staticmethod
    def Generate() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def Encrypt(Phrase:str ,Env_Name:str = 'crypto_key') -> bytes :
        Key = os.environ.get(Env_Name , None)
        if not Key : raise ValueError("crypto_key environment variable is not set")
        frenet = Fernet(Key.encode('utf-8'))
        return frenet.encrypt(Phrase.encode('utf-8'))

    @staticmethod
    def Decrypt(Token:bytes, Env_Name:str = 'crypto_key') -> str :
        Key = os.environ.get(Env_Name , None)
        if not Key : raise ValueError("crypto_key environment variable is not set")
        frenet = Fernet(Key.encode('utf-8'))
        return frenet.decrypt(Token).decode('utf-8')
