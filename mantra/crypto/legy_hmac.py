from struct import pack


def hmac(random_key, body):
    """LegyHmac implementation.

    Args:
        random_key (byte): 128-bit random key
        body (byte): message body

    Returns:
        byte: LegyHmac digest

    """
    if len(random_key) != 16:
        raise Exception("128-bit random_key is needed.")
    b3 = bytearray()
    b4 = bytearray()
    for x in bytearray(random_key):
        y = x ^ 92
        b3.append(y)
        b4.append(y ^ 106)
    b1 = bytearray(b4 + body)
    b2 = bytearray(b3 + pack("!i", _legy_hmac(b1)))
    return pack("!i", _legy_hmac(b2))


def _legy_hmac(message):
    """Custom XXHASH-32 algorithm.

    Ref: https://github.com/Cyan4973/xxHash/wiki/xxHash-specification-(draft)

    Args:
        message (bytearray): bytearray object to hash

    Returns:
        int: int digest

    """
    length = len(message)
    rotate_left = 0
    i = 0
    if length >= 16:
        i2 = 606290984
        i3 = 0
        i4 = 1640531535
        i5 = -2048144777
        while i <= length - 16:
            i2 = _rol(i2 + (_round(message, i) * -2048144777), 13) * -1640531535
            i += 4
            i5 = _rol(i5 + (_round(message, i) * -2048144777), 13) * -1640531535
            i += 4
            i3 = _rol(i3 + (_round(message, i) * -2048144777), 13) * -1640531535
            i += 4
            i4 = _rol(i4 + (_round(message, i) * -2048144777), 13) * -1640531535
            i += 4
        rotate_left = ((_rol(i2, 1) + _rol(i5, 7)) + _rol(i3, 12)) + _rol(i4, 18)
    else:
        rotate_left = 374761393

    rotate_left += length
    while i <= length - 4:
        rotate_left = (
            _rol(rotate_left + (_round(message, i) * -1028477379), 17) * 668265263
        )
        i += 4
    while i < length:
        rotate_left = (
            _rol(rotate_left + ((message[i] & 255) * 374761393), 11) * -1640531535
        )
        i += 1

    result = (_logical_right_shift(rotate_left, 15) ^ rotate_left) * -2048144777
    result = (result ^ _logical_right_shift(result, 13)) * -1028477379
    result = result ^ _logical_right_shift(result, 16)
    return _sign_32(result)


def _mask(n):
    if n >= 0:
        return 2 ** n - 1
    else:
        return 0


def _rotate_left(n, rotations=1, width=32):
    rotations %= width
    if rotations < 1:
        return n
    n &= _mask(width)
    return ((n << rotations) & _mask(width)) | (n >> (width - rotations))


def _rol(i, rotate, max_bits=32):
    """Compact bitwise rotation / circular shift.

    Ref: http://www.falatic.com/index.php/108/python-and-bitwise-rotation

    """
    return (
        (i << rotate % max_bits) & (2 ** max_bits - 1)
        | (i & (2 ** max_bits - 1)) >> (max_bits - (rotate % max_bits))
    )


def _logical_right_shift(val, n):
    return (val % 0x100000000) >> n


def _round(message, i):
    res = (
        ((message[i + 3] & 255) << 24)
        | ((message[i] & 255) | ((message[i + 1] & 255) << 8))
        | ((message[i + 2] & 255) << 16)
    )
    return res


def _sign_32(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000
