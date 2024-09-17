import random
import string

def Password_Generator(length):
    while True:
        chars = (string.ascii_letters + string.digits + '!@#$%&*+').replace('I','T').replace('l','q')
        yield ''.join(random.choice(chars) for _ in range(length))