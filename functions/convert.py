from cryptography.fernet import Fernet

def Encrypt(Phrase:str, Key:bytes, Encoding='utf-8') -> bytes:
    frenet = Fernet(Key)
    return frenet.encrypt(Phrase.encode(Encoding))

def Decrypt(Token:bytes, Key:bytes, Encoding='utf-8') -> str:
    frenet = Fernet(Key)
    return frenet.decrypt(Token).decode(Encoding)

__all__ = [
    'Encrypt',
    'Decrypt',
]