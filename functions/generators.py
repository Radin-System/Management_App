import random
import string

def Generate_Password(Length:int=10,*,
        Ascii:bool = True, 
        Digits:bool = True, 
        Special:bool = True,
        ) -> str:

    Chars = ''
    if Ascii: Chars += string.ascii_letters
    if Digits: Chars += string.digits
    if Special: Chars += string.punctuation

    return ''.join(random.choice(Chars) for _ in range(Length))