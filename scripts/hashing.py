import hashlib
import base64
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hash the given str in base64.')
    parser.add_argument('message', metavar='message', type=str,
                        help='a string message to hash')
    args = parser.parse_args()
    abc =  base64.b64encode(hashlib.sha512(args.message.encode('utf-8')).digest())
    print(str(abc))