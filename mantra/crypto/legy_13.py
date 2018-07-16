# -*- coding: utf-8 -*-
from base64 import b64decode
from struct import pack

from Crypto.Cipher import AES
from Crypto.Util import Padding

from .legy_hmac import hmac

# Obtained via reverse engineering
FIXED_IV = b64decode(b"TglIPjj1/3KAEnue+1wtMw==")


def _compress_int(i):
    return pack("!b", (i >> 8) & 255) + pack("!b", i & 255)


def encrypt(random_key, body):
    # if isinstance(accessToken, str):
    #     accessToken = accessToken.encode()

    header = []
    header.append(_compress_int(0))
    # j = b"X-Line-Access"
    # header.append(_compress_int(len(j)))
    # header.append(j)
    # header.append(_compress_int(len(accessToken)))
    # header.append(accessToken)
    headerByte = b''.join(header)

    raw_body = _compress_int(len(headerByte)) + headerByte + body

    aes = AES.new(random_key, AES.MODE_CBC, FIXED_IV)
    enc_body = aes.encrypt(Padding.pad(raw_body, 16))
    return enc_body + hmac(random_key, enc_body)


def decrypt(random_key, body):
    aes = AES.new(random_key, AES.MODE_CBC, FIXED_IV)

    # The last 4 byte is hmac digest and should be excluded
    dec_body = Padding.unpad(aes.decrypt(body[:-4]), 16)
    # The first 4 byte is header information
    return dec_body[4:]
