# -*- coding: utf-8 -*-
import time
import json
import random
import functools
import weakref
import datetime
from aiohttp import streamer as aiostreamer, StreamReader
from base64 import b64encode, b64decode
from Crypto.Hash import SHA, HMAC, MD5


def generateAccessToken(authToken):
    try:
        authToken = authToken.encode("utf-8")
    except AttributeError:
        pass
    split = authToken.split(b":")
    if len(split) == 2:
        str1 = split[0]
        m = None
        str2 = split[1]
    elif len(split) == 3:
        str1 = split[0]
        m = split[1]
        str2 = split[2]
    else:
        raise Exception("Invalid authToken string: " + authToken)

    currentMillis = int(round(time.time() * 1000))
    str3 = b64encode(b"iat: %d\n" % currentMillis) + b"."
    hmac = HMAC.new(b64decode(str2), str3, SHA)
    str4 = b64encode(hmac.digest())
    str5 = str3 + b"." + str4
    if m is None:
        return (str1 + b":" + str5).decode("utf-8")
    else:
        return (str1 + b":" + m + b":" + str5).decode("utf-8")


def generateAndroidId():
    androidId = ""
    seed = "1234567890asdfghjklzxcvbnmqwertyuiop"
    for _ in range(16):
            androidId += random.choice(seed)
    return androidId


def generateImei(tac="35733507"):
    """http://en.wikipedia.org/wiki/Luhn_algorithm"""
    imei = []
    for i in range(14):
        try:
            digit = tac[i]
        except IndexError:
            digit = random.randint(0, 9)

        imei.append(str(digit))
    imei = ''.join(imei)
    digits = list(map(int, imei + "0"))
    checksum = ((sum(digits[-1::-2])) +
                sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])) % 10
    return imei + str((10 - checksum) % 10)


def generateUdidHash():
    return (MD5.new(bytes(generateAndroidId(), "utf-8")).hexdigest(),
            MD5.new(bytes(generateImei(), "utf-8")).hexdigest())


def generateOid(z=False, z2=False):
    androidId = generateAndroidId()
    times = timestampToDate(time.time())
    return MD5.new(f"{androidId}{times}".encode()).hexdigest()


def timestampToDate(timestamp, millis=False):
    timestamp = timestamp if millis is False else timestamp / 1000
    return datetime.datetime.utcfromtimestamp(
        timestamp).strftime('%Y-%m-%d %H:%M:%S')


@aiostreamer
async def streamer(writer, data):
    if isinstance(data, StreamReader):
        chunk = await data.read(524288)
        while chunk:
            await writer.write(chunk)
            chunk = await data.read(524288)
    else:
        await writer.write(data)


def memoized_method(*lru_args, **lru_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            # We're storing the wrapped method inside the instance. If we had
            # a strong reference to self the instance would never die.
            self_weak = weakref.ref(self)
            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)
            setattr(self, func.__name__, cached_method)
            return cached_method(*args, **kwargs)
        return wrapped_func
    return decorator


def parseMention(message, useSet=False):
    if 'MENTION' in message.contentMetadata:
        mentionees = json.loads(message.contentMetadata['MENTION'])['MENTIONEES']
        seen = set()
        result = []
        for x in mentionees:
            if x['M'] not in seen:
                seen.add(x['M'])
                result.append(x['M'])
        return set(result) if useSet is True else result
    else:
        return None


def buildMention(string, mids, key="@!"):
    indexes = findIndex(string, key)
    key_len = len(key)
    if len(indexes) == len(mids):
        base = {"MENTIONEES": []}
        for index, mid in zip(indexes, mids):
            data = {"S": str(index), "E": str(index + key_len), "M": mid}
            base['MENTIONEES'].append(data)
        return {"MENTION": json.dumps(base, separators=(',', ':'))}


def findIndex(string, key):
    start = 0
    result = []
    while True:
        start = string.find(key, start)
        if start == -1:
            return result
        result.append(start)
        start += len(key)
