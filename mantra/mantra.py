# -*- coding: utf-8 -*-
import re
import rsa
import inspect
import socket

from uvloop import new_event_loop

# from pulsar.apps import http
from multidict import CIMultiDict
from aiohttp import TCPConnector
from aiohttp.resolver import AsyncResolver

from . import client, util
from .lib.aiohttp import ClientSession
from .constant import SERVICE, LEGY, APP, OBS, VERIFICATION_PATH
from .api import LineApi
from .service.ttypes import (
    IdentityProvider,
    LoginResultType,
    LoginRequest,
    LoginType,
    TalkException,
    AccountMigrationCheckType,
    DeviceInfo,
    CarrierCode,
)
from .ch.timeline import Timeline
from .apps import JunglePang, Tenor

IS_EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class Mantra(LineApi):
    OBS = None
    LEGY = None

    def __init__(self, loop=None, session=None, geo="JP"):
        self.loop = loop or new_event_loop()
        self.session = None
        self.protocol = None
        self.logged_in = False

        self.mid = None
        self._setting = {
            "auth": {"cert": None, "key": None, "token": None, "type": None}
        }

        if session is None:
            # explicitly use async resolver to keep aiohttp from using threaded
            # resolver, which causing memory leak (or not) because the spawned
            # thread doesn't terminate.
            dns = AsyncResolver(loop=self.loop)
            tcp = TCPConnector(
                ssl=False,
                loop=self.loop,
                resolver=dns,
                # AsyncResolver has problems related to domains with ipv6
                # https://github.com/aio-libs/aiohttp/issues/2522
                family=socket.AF_INET,
            )
            skip_headers = ["Accept-Encoding"]
            self.session = ClientSession(
                loop=self.loop, connector=tcp, skip_auto_headers=skip_headers
            )
        else:
            self.session = session

        self.session._default_headers = CIMultiDict(
            {"connection": "keep-alive", "Accept": "*/*"}
        )
        self.session._headers = CIMultiDict()

        Mantra.OBS = OBS[geo]
        Mantra.LEGY = LEGY[geo]

    @property
    def authKey(self):
        return self._setting["auth"]["authKey"]

    @authKey.setter
    def authKey(self, value):
        self._setting["auth"]["authKey"] = value

    @property
    def authToken(self):
        return self._setting["auth"]["token"]

    @authToken.setter
    def authToken(self, value):
        self._setting["auth"]["token"] = value

    def _validate(self, mail, passwd, cert, token, qr, key, sns):
        if mail is not None and passwd is not None and cert is None:
            return 1
        elif mail is not None and passwd is not None and cert is not None:
            return 2
        elif token is not None and sns is None:
            return 3
        elif qr is True:
            return 4
        elif key is not None:
            return 5
        elif token is not None and sns is not None:
            return 6
        else:
            return -1

    async def login(
        self,
        identity=None,
        password=None,
        cert=None,
        token=None,
        qr=False,
        key=None,
        callback=print,
        clientType="win10",
        protocol="binary",
        sns=None,
        ssl=True,
        **kw
    ):

        url = ("https://" if ssl else "http://") + self.LEGY

        self.Auth = client.auth(
            url + SERVICE[protocol]["REGISTRATION"], self.session, protocol
        )

        self.session._headers.update(
            {
                "User-Agent": APP[clientType]["UserAgent"],
                "X-Line-Application": APP[clientType]["LineApplication"],
            }
        )

        self.protocol = protocol
        self.clientType = clientType

        loginType = self._validate(identity, password, cert, token, qr, key, sns)

        try:
            if loginType == 1:
                await self._login(identity, password, callback=callback)
            elif loginType == 2:
                await self._login(identity, password, cert, callback=callback)
            elif loginType == 3:
                self.tokenLogin(token)
            elif loginType == 4:
                await self.qrLogin(callback=callback)
            elif loginType == 5:
                try:
                    await self.keyLogin(key)
                except Exception:
                    raise
            elif loginType == 6:
                await self.loginWithSns(sns, token)
            else:
                raise Exception("Invalid arguments")
        except TalkException as e:
            raise

        # iPad can't use binary normal path
        if clientType == "ipad" and protocol == "binary":
            # aiohttp have a problem with long polling path, polling
            # request often get stuck. Should revisit this issue since
            # urllib doesn't have this problem.
            pollpath = "NORMAL_POLLING"
            talkpath = "NOTIFY_SLEEP"
        else:
            talkpath = "NORMAL"
            pollpath = "LONG_POLLING"

        self.Talk = client.talk(
            url + SERVICE[protocol][talkpath], self.session, protocol
        )

        self.Poll = client.poll(
            url + SERVICE[protocol][pollpath], self.session, protocol
        )
        # self.Poll.trans.updateCustomHeaders({"Connection": "close"})

        self.Channel = client.channel(
            url + SERVICE[protocol]["CHANNEL"], self.session, protocol
        )
        self.Call = client.call(url + SERVICE[protocol]["CALL"], self.session, protocol)
        self.Liff = client.liff(url + SERVICE["compact"]["LIFF"], self.session)

        self.mid = (await self.Talk.getProfile()).mid

        # Init channel
        self.Timeline = Timeline(self)
        try:
            await self.Timeline.login()
        except Exception:
            pass

        # Init Chat apps
        # self.Tenor = Tenor(self)
        self.JunglePang = JunglePang(self)
        try:
            await self.JunglePang.login()
        except Exception:
            pass

        await self.sync()
        self.logged_in = True

    async def _login(self, identity, password, cert=None, callback=print):
        self.Auth.trans.path = SERVICE[self.protocol]["REGISTRATION"]

        if IS_EMAIL.match(identity):
            identityProvider = IdentityProvider.LINE
        else:
            identityProvider = IdentityProvider.LINE_PHONE

        rsainfo = await self.Auth.getRSAKeyInfo(identityProvider)
        message = (
            chr(len(rsainfo.sessionKey)) + rsainfo.sessionKey +
            chr(len(identity)) + identity +
            chr(len(password)) + password
        ).encode("utf-8")
        publicKey = rsa.PublicKey(int(rsainfo.nvalue, 16), int(rsainfo.evalue, 16))
        crypto = rsa.encrypt(message, publicKey).hex()

        self.Auth.trans.path = SERVICE[self.protocol]["AUTH_REGISTRATION"]

        loginRequest = LoginRequest(
            type=LoginType.ID_CREDENTIAL,
            identityProvider=identityProvider,
            identifier=rsainfo.keynm,
            password=crypto,
            keepLoggedIn=True,
            accessLocation=None,
            systemName="Mantra",
            certificate=cert,
            verifier=None,
            secret=None,
            e2eeVersion=0,
        )
        loginResult = await self.Auth.loginZ(loginRequest)

        if loginResult.type == LoginResultType.SUCCESS:
            self.certificate = loginResult.certificate
            self.tokenLogin(loginResult.authToken)

        elif loginResult.type == LoginResultType.REQUIRE_QRCODE:
            await self.qrLogin(callback=callback)

        elif loginResult.type == LoginResultType.REQUIRE_DEVICE_CONFIRM:
            if inspect.iscoroutinefunction(callback):
                await callback(loginResult.verifier + ":" + loginResult.pinCode)
            else:
                callback(loginResult.verifier + ":" + loginResult.pinCode)
            header = {
                "X-Line-Application": APP[self.clientType]["LineApplication"],
                "X-Line-Access": loginResult.verifier,
            }
            url = "https://" + self.LEGY + VERIFICATION_PATH
            result = await self.session.get(url, headers=header)
            result = await result.json()

            loginRequest = LoginRequest(
                LoginType.QRCODE,
                verifier=result["result"]["verifier"],
            )
            loginResult = await self.Auth.loginZ(loginRequest)

            if loginResult.type == LoginResultType.SUCCESS:
                self.certificate = loginResult.certificate
                self.tokenLogin(loginResult.authToken)

        elif loginResult.type == LoginResultType.REQUIRE_SMS_CONFIRM:
            raise Exception("SMS Verfication is not yet implemented!")

    async def qrLogin(self, callback=print, keyLogin=False):
        self.Auth.trans.path = SERVICE[self.protocol]["REGISTRATION"]

        qrCode = await self.Auth.getAuthQrcode(True, "Mantra")
        if keyLogin is True:
            await callback(qrCode.verifier)
        else:
            if inspect.iscoroutinefunction(callback):
                await callback("line://au/q/" + qrCode.verifier)
            else:
                callback("line://au/q/" + qrCode.verifier)

        header = {
            "X-Line-Application": APP[self.clientType]["LineApplication"],
            "X-Line-Access": qrCode.verifier,
        }
        url = "https://" + self.LEGY + VERIFICATION_PATH
        result = await self.session.get(url, headers=header)
        result = await result.json()

        self.Auth.trans.path = SERVICE[self.protocol]["AUTH_REGISTRATION"]

        loginRequest = LoginRequest(
            type=LoginType.QRCODE,
            identityProvider=IdentityProvider.LINE_PHONE,
            verifier=result["result"]["verifier"],
        )
        loginResult = await self.Auth.loginZ(loginRequest)

        if loginResult.type == LoginResultType.SUCCESS:
            self.certificate = loginResult.certificate
            self.tokenLogin(loginResult.authToken)

    async def keyLogin(self, authKey):
        self.authKey = authKey
        self.tokenLogin(util.generateAccessToken(self.authKey))
        if self.clientType not in {"android", "ios", "lite", "tizen"}:

            async def verifyQr(verifier):
                self.Auth.trans.updateDefaultHeaders(
                    {
                        "User-Agent": APP["lite"]["UserAgent"],
                        "X-Line-Application": APP["lite"]["LineApplication"],
                    }
                )
                await self.Auth.verifyQrcode(verifier, None)
                self.Auth.trans.updateDefaultHeaders(
                    {
                        "User-Agent": APP[self.clientType]["UserAgent"],
                        "X-Line-Application": APP[self.clientType]["LineApplication"],
                    }
                )

            await self.qrLogin(verifyQr, True)

    def tokenLogin(self, authToken):
        self.authToken = authToken
        self.session._headers["X-Line-Access"] = self.authToken

    async def loginWithSns(self, snsIdType, accessToken, region="JP"):
        self.Auth.trans.path = self.SERVICE[self.protocol]["REGISTRATION"]
        session = await self.Auth.createAccountMigrationPincodeSession()
        udidHash, oldUdidHash = util.generateUdidHash()
        try:
            userStatus = await self.Auth.findSnsIdUserStatus(
                snsIdType, accessToken, udidHash, session, oldUdidHash
            )
        except TalkException:
            raise

        if userStatus.accountMigrationCheckType == AccountMigrationCheckType.SKIP:
            deviceInfo = DeviceInfo(
                "SM-A310F", "Android OS", "7.0", "SM-A310F", 0, "NOT_SPECIFIED", None
            )
            registration = await self.Auth.registerWithSnsId(
                snsIdType, accessToken, region, udidHash, deviceInfo, None, session
            )
            await self.keyLogin(registration.authToken)

    async def registerWithPhone(self, phone, region):
        self.Auth.trans.path = SERVICE[self.protocol]["REGISTRATION"]
        udidHash, oldUdidHash = util.generateUdidHash()
        deviceInfo = DeviceInfo(
            "SM-A310F", "Android OS", "7.0", "SM-A310F", 0, "NOT_SPECIFIED", None
        )
        verification = await self.Auth.startVerification(
            region,
            CarrierCode.NOT_SPECIFIED,
            phone,
            udidHash,
            deviceInfo,
            "51011",
            None,
            "en_GB",
            None,
            oldUdidHash,
        )
        pinCode = input("Pincode: ")
        await self.Auth.verifyPhoneNumber(
            verification.sessionId, pinCode, udidHash, oldUdidHash
        )
        registration = await self.Auth.registerWithPhoneNumber(
            verification.sessionId, None
        )
        self.certificate = registration.certificate
        await self.keyLogin(registration.authToken)

    async def close(self):
        await self.session.close()
