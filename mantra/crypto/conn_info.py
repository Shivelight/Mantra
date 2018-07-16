# -*- coding: utf-8 -*-
"""Implementation of LINE CONN INFO cryptography based on CONN_INFO.md

Example:

    >>> import secrets, conn_info, requests
    >>> params = conn_info.generate_params('Android_OS', '8.8.0')
    >>> randkey = secrets.token_bytes(16)
    >>> lcs = conn_info.generate_lcs(randkey)
    >>> r = requests.get(".../R3", params=params, headers={'X-LCS': lcs})
    >>> conn_info.verify(randkey, r.headers['x-lcm'], r.content)
    True

"""

from base64 import b64decode
import time

from Crypto.Cipher import AES
from Crypto.Hash import SHA1, MD5
from Crypto.Util.Padding import unpad


# Obtained via reverse engineering
MAGIC_VALUE = b64decode(b"TGBe/989/KEhfUgXQCBWkYDcIzildyqA7QqqAbzQoI8=")
FIXED_IV = b64decode(b"TglIPjj1/3KAEnue+1wtMw==")


def generate_params(type_, version, regions=None, timee=None, carrier=None):
    """Helper function to generate CONN_INFO params with valid key.

    Args:
        type_ (str): Android_OS / iPhone_OS
        version (str): Client version, example: 8.8.0
        regions (str): Region with the following format:
            <SIM ISO 3166 2>--<Country/Region ISO 3166 2/UN M.49>
        carrier (str): SIM MCC+MNC
        timee (str): Time in millis

    Returns:
        dict: Params with valid key.

    """
    regions = regions or "JP--JP"
    timee = timee or str(int(time.time() * 1000))
    carrier = carrier or "(null)(null)"
    key = _generate_conn_info_key(type_, version, regions, timee, carrier)
    params = {
        "type": type_,
        "version": version,
        "regions": regions,
        "time": timee,
        "carrier": carrier,
        "key": key,
    }
    return params


def _generate_conn_info_key(type_, version, regions, timee, carrier):
    """Generate a valid params key."""
    params = f"{type_}{version}{regions}{timee}{carrier}"
    return MD5.new(params.encode() + MAGIC_VALUE).hexdigest()


def verify(random_key, lcm, body):
    """Verify if the body has not tampered.

    Args:
        random_key (byte): 16 byte random key, must be the same as X-LCS.
        lcm (str): Oobtained from x-lcm header.
        body (byte): Response body.

    Returns:
        bool: True if the body is valid else False.

    """
    if isinstance(body, str):
        body = body.encode()
    aes = AES.new(random_key, AES.MODE_CBC, FIXED_IV)
    server_digest = unpad(aes.decrypt(b64decode(lcm)), 32)
    client_digest = SHA1.new(body).digest()
    return server_digest == client_digest
