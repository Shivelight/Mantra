# -*- coding: utf-8 -*-

from .service.ttypes import LiffViewRequest, LiffContext, LiffChatContext
from .util import memoized_method

JP_URL = "https://game.linefriends.com/jbp-lcs-ranking"


class JunglePang(object):

    def __init__(self, mantra):
        self.mantra = mantra
        self.cc = None

    async def login(self):
        token = await self.mantra.Channel.issueChannelToken('1526709289')
        self.cc = token.token

    async def membersExist(self, id_, type_='group'):
        data = {'cc': self.cc, 'type': type, 'id': id_}
        url = f"{JP_URL}/lcs/membersExist"
        result = await self.mantra.session.post(url, json=data)
        return await result.json()['exists']

    async def myRank(self, id_):
        data = {'ClientID': id_, 'cc': self.cc, 'nomd5': True}
        url = f"{JP_URL}/rank/my_rank"
        result = await self.mantra.session.post(url, json=data)
        return await result.json()

    async def rankByScore(self, id_, score, size=50):
        data = {'ClientID': id_, 'Score': score, 'ListSize': size}
        url = f"{JP_URL}/rank/rank_by_score"
        result = await self.mantra.session.post(url, json=data)
        return await result.json()

    async def addScoreWithToken(self, id_, score):
        data = {'ClientID': id_, 'Score': score, 'cc': self.cc, 'nomd5': True}
        url = f"{JP_URL}/rank/add_score_with_token"
        result = await self.mantra.session.post(url, json=data)
        return await result.json()

    async def uploadImage(self, path):
        url = f"{JP_URL}/lcs/imageUpload"
        with open(path, 'rb') as f:
            result = await self.mantra.session.post(url, data=f)
        return await result.json()['x-obs-hash']

    async def sendMessage(self, to, messages):
        data = {
            'cc': self.cc,
            'to': to,
            'messages': messages
        }

        url = f"{JP_URL}/lcs/sendMessage"
        result = await self.mantra.session.post(url, json=data)
        res = await result.json()
        if res.get('status') != "ok":
            raise Exception("Failed to send message.")


class Tenor(object):

    def __init__(self, mantra):
        self.mantra = mantra

    async def issueBearer(self, to):
        context = LiffContext(LiffChatContext(to))
        req = LiffViewRequest('1562242036-RW04okm', context)
        view = await self.mantra.Liff.issueLiffView(req)
        return view.accessToken

    async def auth(self):
        headers = {
            'access-control-request-headers': 'authorization, content-type',
            'access-control-request-method': 'POST',
            'origin': 'https://line-app.tenor.com',
        }
        url = "https://webview-helpers.tenor.com/line-proxy/message/v3/share"
        result = await self.mantra.session.options(url, headers=headers)
        if result.status_code != 204:
            raise Exception("Failed to auth.")

    async def share(self, bearer, messages):
        print(bearer)
        # await self.auth()
        headers = {
            'Authorization': f"Bearer {bearer}",
            'origin': "https://line-app.tenor.com",
        }
        data = {'messages': messages}
        url = "https://webview-helpers.tenor.com/line-proxy/message/v3/share"
        result = await self.mantra.session.post(url, headers=headers, json=data)
        if result.status_code != 200:
            raise Exception("Failed to share message.")
