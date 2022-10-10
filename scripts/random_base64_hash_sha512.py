import hashlib
import base64
import random
import pyperclip

def get_random_b64_sha512(max_int=10000000000000):
    return base64.b64encode(hashlib.sha512(str(random.randint(0, 10000000000000)).encode('utf-8')).digest())


if __name__ == '__main__':
    result = str(base64.b64encode(hashlib.sha512(str(random.randint(0, 10000000000000)).encode('utf-8')).digest()))
    pyperclip.copy(result[2:-1])
    print(result)