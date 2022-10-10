#!/usr/bin/env python3.10
import requests
import json
import random
import base64
from hashlib import sha256, sha512
from os import getenv, sep
from time import sleep

from dotenv import load_dotenv, find_dotenv

# Load env data
load_dotenv(find_dotenv())

API_ENDPOINT = getenv('API_ENDPOINT')
RPUUID = getenv('RPUUID')
RPNAME = getenv('RPNAME')

HEADERS = {'Content-Type': 'application/json'}


def get_document_hash(fn):
    doc_hash = ''
    with open(fn, 'rb') as f:
        doc_hash = base64.b64encode(sha512(f.read()).digest())
    return doc_hash


def load_template(template):
    template_json = {}
    with open('templates' + sep + template + '.json', 'r') as f:
        template_json = json.loads(f.read())
    template_json['relyingPartyUUID'] = RPUUID
    template_json['relyingPartyName'] = RPNAME
    return template_json


def authentication_request(personal_code):
    sessionID = ''
    auth_hash = base64.b64encode(sha512(personal_code.encode('ascii') +
                                        random.randbytes(512)).digest())
    auth_json = load_template('authentication_template')
    auth_json['hash'] = auth_hash.decode('ascii')
    url = API_ENDPOINT + 'authentication/etsi/PNOEE-' + str(personal_code)
    r = requests.post(url, data=json.dumps(
        auth_json, indent=2), headers=HEADERS)
    if r.status_code == 200:
        sessionID = r.json()['sessionID']
    return sessionID


def signature_request(doc_number, hash_to_sign):
    sessionID = ''
    auth_json = load_template('signature_template')
    auth_json['hash'] = hash_to_sign.decode('ascii')
    url = API_ENDPOINT + 'signature/document/' + doc_number
    r = requests.post(url, data=json.dumps(
        auth_json, indent=2), headers=HEADERS)
    if r.status_code == 200:
        sessionID = r.json()['sessionID']
    return sessionID


def session_status(sessionID):
    result = ''
    url = API_ENDPOINT + 'session/' + sessionID
    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()
    return result


def verify_signature(signature):
    # https://github.com/SK-EID/smart-id-documentation/blob/master/README.md#23123-verifying-the-authentication-response
    # 1. result.endResult has the value OK
    # 2. he certificate from cert.value is valid:
    #       The certificate is trusted (signed by a trusted CA).
    #       The certificate has not expired.
    # 3. The person's certificate given in the cert.value is of required or higher assurance level as requested.
    # 4. The identity of the authenticated person is in the subject field or subjectAltName extension of the X.509 certificate.
    # 5. signature.value is the valid signature over the same hash, which was submitted by the RP verified using the public key from cert.value
    return False


def get_vc(auth_hash):
    return int.from_bytes((sha256(base64.b64decode((auth_hash))).digest())[-2:], "big") % 10000


if __name__ == '__main__':
    print('Starting...')
    session_id = authentication_request('30303039903')
    document_number = ''
    while document_number == '':
        try:
            session = session_status(session_id)
            document_number = session['result']['documentNumber']
        except:
            # not completed yet
            print('not completed yet')
            sleep(1)
    print(document_number)
    hash_to_sign = get_document_hash('dummy.txt')
    vc = get_vc(hash_to_sign)
    print('vc:', vc)
    session_id = signature_request(
        document_number, hash_to_sign)
    doc_signed = ''
    while doc_signed == '':
        try:
            session = session_status(session_id)
            doc_signed = session['signature']['value']
        except:
            # not completed yet
            print('not completed yet signature')
            sleep(1)
    print(doc_signed)
