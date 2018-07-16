# -*- coding: utf-8 -*-
from base64 import b64encode
import os

from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.PublicKey import RSA


keys_path = os.path.dirname(os.path.abspath(__file__)) + "/keys"

rsa_0004 = os.path.join(keys_path, "lcs_0004.key")
with open(rsa_0004) as public_key:
    _cipher_0004 = PKCS1_OAEP.new(RSA.import_key(public_key.read()))
    del rsa_0004

rsa_0007 = os.path.join(keys_path, "lcs_0007.key")
with open(rsa_0007) as public_key:
    _cipher_0007 = PKCS1_v1_5.new(RSA.import_key(public_key.read()))
    del rsa_0007

rsa_0008 = os.path.join(keys_path, "lcs_0008.key")
with open(rsa_0008) as public_key:
    _cipher_0008 = PKCS1_v1_5.new(RSA.import_key(public_key.read()))
    del rsa_0008

del os, RSA, PKCS1_OAEP, PKCS1_v1_5, keys_path


def gen_0004(random_key):
    data = _cipher_0004.encrypt(random_key)
    return "0004" + b64encode(data).decode()


def gen_0007(random_key):
    data = _cipher_0007.encrypt(random_key)
    return "0007" + b64encode(data).decode()


def gen_0008(random_key):
    data = _cipher_0008.encrypt(random_key)
    return "0008" + b64encode(data).decode()
