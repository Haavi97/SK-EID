import hashlib
import argparse

def get_smart_id_code(hash):
    result = int.from_bytes(hashlib.sha512(str(hash).encode('utf-8')).digest(), "big")
    # int(hashlib.sha512(str(hash).encode('utf-8')).hexdigest(), base=16)
    # Alternative, I guess slower
    return result%1000

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the Smart ID code for the given hash')
    parser.add_argument('hash', metavar='hash', type=str,
                        help='string hash')
    args = parser.parse_args()
    print(get_smart_id_code(args.hash))