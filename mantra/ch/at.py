# -*- coding: utf-8 -*-
import time

from ..constant import PUBLIC_LINE_CMS_PATH, APP


class At(object):
    def __init__(self, mantra):
        self.mantra = mantra
        self.token = None
        self.obsToken = None
        self.refreshToken = None
        self.channelAccessToken = None
        self.cmsToken = None
        self.cmsRefreshToken = None
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Line/1.7.2",
            "X-Line-Application": APP["bizandroid"]["lineApplication"],
        }
        self.CMS = f"https://{mantra.LEGY}{PUBLIC_LINE_CMS_PATH}/api/core"

    @property
    def mid(self):
        return self.mantra.mid

    @property
    def client(self):
        return self.mantra.Channel

    @property
    def session(self):
        return self.mantra.session

    async def login(self):
        channelToken = await self.client.issueChannelToken("1417913499")
        self.token = channelToken.token
        self.obsToken = channelToken.obsToken
        self.refreshToken = channelToken.refreshToken
        self.channelAccessToken = channelToken.channelAccessToken
        self.headers["X-Line-ChannelToken"] = self.channelAccessToken

    async def issueCMSToken(self, udidHash):
        url = f"{self.CMS}/auth/cmsToken"
        data = {"channelAccessToken": self.channelAccessToken, "udidHash": udidHash}
        result = await self.session.post(url, json=data, headers=self.headers)
        if result != 200:
            raise Exception("Cannot issue CMSToken", await result.text())
        token = await result.json()
        self.cmsToken = token['accessToken']
        self.cmsRefreshToken = token['refreshToken']
        self.headers["X-CMSToken"] = self.cmsToken

    async def refreshCMSToken(self):
        url = f"{self.CMS}/auth/cmsToken?refresh"
        data = {"refreshToken": self.cmsRefreshToken}
        result = await self.session.post(url, json=data, headers=self.headers)
        if result != 200:
            raise Exception("Cannot refresh CMSToken", await result.text())
        token = await result.json()
        self.cmsToken = token['accessToken']
        self.cmsRefreshToken = token['refreshToken']
        self.headers["X-CMSToken"] = self.cmsToken

    async def registerPublicAccount(
        self,
        country,
        deviceInfo,
        displayName,
        majorCategory,
        minorCategory,
        registerToken,
        ageVerified,
        udidHash,
    ):
        url = f"{self.CMS}/account/register"
        data = {
            "country": country,
            "deviceInfo": deviceInfo,
            "displayName": displayName,
            "majorCategory": majorCategory,
            "minorCategory": minorCategory,
            "registerToken": registerToken,
            "ageVerified": ageVerified,
        }
        data["deviceInfo"]["udidHash"] = udidHash
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def issueUdidHash(self, deviceInfo, deviceUid):
        url = f"{self.CMS}/device/issueUdid"
        data = {"deviceInfo": deviceInfo, "deviceUid": deviceUid}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def issueLINEAccessToken(self, botMid, deviceInfo, udidHash):
        url = f"{self.CMS}/auth/lineToken"
        data = {"botMid": botMid, "deviceInfo": deviceInfo}
        data["deviceInfo"]["udidHash"] = udidHash
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def issueAtCCCookie(self, botMid, channelId="1418234097"):
        url = f"{self.CMS}/auth/atCC/{channelId}"
        data = {"botMid": botMid}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def logout(self, udidHash):
        url = f"{self.CMS}/auth/logout"
        data = {"udidHash": udidHash}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def resign(self):
        url = f"{self.CMS}/account/resign"
        data = {"resignToken": int(time.time() * 1000)}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def notifyUpdateOfProfileImage(self, botMid):
        url = f"{self.CMS}/account/profileImage/notify"
        data = {"botMid": botMid}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def updateNotificationToken(self, token, type_):
        url = f"{self.CMS}/notify/token"
        data = {"token": token, "type": type_}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def invalidateNotificationToken(self, type_):
        url = f"{self.CMS}/notify/token"
        data = {"type": type_}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def adjustBadgeCount(self, str2, lastRevision, badge):
        url = f"{self.CMS}/account/badge/adjust/{str2}"
        data = {"lastRevision": lastRevision, "badge": badge}
        result = await self.session.post(url, json=data, headers=self.headers)
        return await result.json()

    async def getMemberList(self):
        url = f"{self.CMS}/account/members"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getAccountList(self, notification="1", order="new"):
        url = f"{self.CMS}/account/list"
        params = {"notification": notification, "order": order}
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def prepareToRegisterNewAccount(self):
        url = f"{self.CMS}/account/prepare"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getMoreTabMenu(self):
        url = f"{self.CMS}/cms/top"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getTrackingInformation(self):
        url = f"{self.CMS}/account/measure"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getCouponList(self):
        url = f"{self.CMS}/cms/coupon"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getNoticeAgreementAvailability(self):
        url = f"{self.CMS}/account/availability"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def getChatRoomPlusDynamicMenu(self):
        url = f"{self.CMS}/account/plusMenu"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    def getDeviceInfo(self, deviceName, model):
        return {"deviceName": deviceName, "model": model}
