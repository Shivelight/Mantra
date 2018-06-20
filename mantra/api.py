# -*- coding: utf-8 -*-
from os.path import basename, getsize
from base64 import b64encode
import json
import random

from .lib.aiohttp import ClientResponse
from .service.ttypes import Message
from .util import streamer


class LineApi(object):

    async def stream(self, amount=1):
        # ops = await self.client.fetchOps(self.revision, amount, 0, 0)
        ops = await self.Poll.fetchOperations(self.revision, amount)
        self.revision = max(self.revision, max([op.revision for op in ops]))
        return ops

    async def sync(self):
        self.revision = await self.Talk.getLastOpRevision()

    async def deleteContact(self, mid):
        await self.Talk.updateContactSetting(0, mid, 16, 'true')

    async def forwardMessage(self, to, message):
        msg = await self.Talk.sendMessage(
            0, Message(to=to, text=f"{message.text}\u200b",
                       location=message.location,
                       contentType=message.contentType,
                       contentMetadata=message.contentMetadata)
        )
        if message.contentType not in {1, 2}:
            return
        params = {
            "oid": msg.id,
            "type": "",
            "copyFrom": f"/os/m/{message.id}",
        }
        headers = {**self.session._headers, **{
            "Content-Type": "application/x-www-form-urlencoded",
        }}
        url = f"http://{self.OBS}/talk/m/copy.nhn"
        result = await self.session.post(url, params=params, headers=headers)
        if result.status_code != 200:
            raise Exception("Failed to forward message.")

    async def changeProfilePicture(self, obj, vp=False):
        if isinstance(obj, ClientResponse):
            length = int(obj.headers['Content-Length'])
            data = obj.content
        else:
            data = open(data, 'rb').read()
            length = len(data)
        # params = {
        #     'type': 'image'
        # }
        # url = f"http://{self.OBS}/r/talk/p/{self.mid}"
        headers = {
            "Content-Type": "image/jpeg",
            "Content-Length": str(length)
        }
        if vp:
            params = {
                'name': 'vp.jpg',
                'cat': 'vp.mp4',
                'type': 'image',
                'ver': '2.0'
            }
            obs = b64encode(json.dumps(params).encode()).decode()
            headers.update({'x-obs-params': obs})
            url = f"http://{self.OBS}/r/talk/p/{self.mid}"
        else:
            url = f"http://{self.OBS}/os/p/{self.mid}"
        headers.update(self.session._headers)
        result = await self.session.post(url, data=streamer(data=data),
                                         headers=headers)
        if result.status != 201:
            raise Exception("Failed to change profile picture.")

    async def changeProfileVideo(self, obj, picobj):
        if isinstance(obj, ClientResponse):
            length = int(obj.headers['Content-Length'])
            data = obj.content
        else:
            data = open(data, 'rb').read()
            length = len(data)
        params = {
            'name': 'vp.mp4',
            'cat': 'vp.mp4',
            'type': 'video',
            'ver': '2.0',
        }
        headers = {
            "Content-Type": "video/mp4",
            "Content-Length": str(length),
            "x-obs-params": b64encode(json.dumps(params).encode()).decode(),
        }
        headers.update(self.session._headers)
        url = f"http://{self.OBS}/r/talk/vp/{self.mid}"
        result = await self.session.post(url, data=streamer(data=data),
                                         headers=headers)
        if result.status != 201:
            raise Exception("Failed to change profile video.")
        await self.changeProfilePicture(picobj, vp=True)

    async def sendMediaToTalk(self, to, path, ttype):
        pass

    async def sendAudio(self, to, path):
        size = getsize(path)
        params = {
            "duration": "10000",
            "name": "0",
            "oid": "reqseq",
            "reqseq": "0",
            "range": f"bytes 0-{size - 1}/{size}",
            "tomid": to,
            "type": "audio",
            "ver": "1.0"
        }
        headers = {
            "Content-Type": "audio/aac",
            "x-obs-params": b64encode(json.dumps(params).encode()).decode()
        }
        headers.update(self.session._headers)
        url = f"https://{self.OBS}/r/talk/m/reqseq"
        with open(path, 'rb') as f:
            result = await self.session.post(url, data=f.read(),
                                             headers=headers)
        if result.status_code != 201:
            raise Exception("Failed to upload audio.")

    async def sendAudioWithUrl(self, to, url):
        result = await self.session.get(url)
        await self.sendAudio(to, result)

    async def sendContact(self, to, mid):
        message = Message(to=to, contentType=13, contentMetadata={"mid": mid})
        await self.Talk.sendMessage(0, message)

    async def sendPresent(self, mid, package='', prd='STICKER',
                          ver='1', tpl=None):
        if tpl is None:
            tpl = str(random.choice(range(1, 10)))
        meta = {
            'STKPKGID': package,
            'MSGTPL': tpl,
            'PRDTYPE': prd,
            'STKVER': ver
        }
        message = Message(to=mid)
        message.contentType = 9
        message.contentMetadata = meta
        await self.Talk.sendMessage(0, message)

    async def sendFile(self, to, path):
        name = basename(path)
        size = getsize(path)
        params = {
            "name": name,
            "oid": "reqseq",
            "reqseq": "0",
            "range": f"bytes 0-{size-1}/{size}",
            "tomid": to,
            "type": "file",
            "ver": "1.0"
        }
        headers = {
            "Content-Type": "",
            "x-obs-params": b64encode(json.dumps(params).encode()).decode()
        }
        headers.update(self.session._headers)
        url = f"https://{self.OBS}/r/talk/m/reqseq"
        with open(path, 'rb') as f:
            result = await self.session.post(url, data=f.read(), headers=headers)
        if result.status_code != 201:
            raise Exception("Failed to upload file.")

    async def sendFileWithUrl(self, to, url):
        result = await self.session.get(url)
        await self.sendFile(to, result)

    async def sendGif(self, to, path):
        size = getsize(path)
        params = {
            "cat": "original",
            "name": "0",
            "oid": "reqseq",
            "quality": "100",
            "reqseq": "0",
            "range": f"bytes 0-{size - 1}/{size}",
            "tomid": to,
            "type": "image",
            "ver": "1.0"
        }
        headers = {
            "Content-Type": "image/gif",
            "x-obs-params": b64encode(json.dumps(params).encode()).decode()
        }
        headers.update(self.session._headers)
        url = f"https://{self.OBS}/r/talk/m/reqseq"
        result = await self.session.post(url, data=data, headers=headers)
        if result.status_code != 201:
            raise Exception("Failed to upload gif.")

    async def sendGifWithUrl(self, to, url):
        result = await self.session.get(url)
        await self.sendGif(to, result)

    async def sendImage(self, to, obj):
        if isinstance(obj, ClientResponse):
            length = int(obj.headers['Content-Length'])
            data = obj.content
        else:
            data = open(data, 'rb').read()
            length = len(data)
        params = {
            "name": "0",
            "oid": "reqseq",
            "quality": "100",
            "range": "bytes 0-{}/{}".format(length - 1, length),
            "reqseq": "0",
            "tomid": to,
            "type": "image",
            "ver": "1.0"
        }
        headers = {
            "Content-Type": "image/jpeg",
            "Content-Length": str(length),
            "x-obs-params": b64encode(json.dumps(params).encode()).decode()
        }
        headers.update(self.session._headers)
        url = f"https://{self.OBS}/r/talk/m/reqseq"
        result = await self.session.post(url, data=streamer(data=data),
                                         headers=headers)
        if result.status != 201:
            raise Exception("Failed to upload image.")

    async def sendImageWithUrl(self, to, url):
        result = await self.session.get(url)
        await self.sendImage(to, result)

    async def sendVideo(self, to, obj):
        if isinstance(obj, ClientResponse):
            length = int(obj.headers['Content-Length'])
            data = obj.content
        else:
            data = open(data, 'rb').read()
            length = len(data)
        params = {
            "duration": "",
            "name": "0.t.mp4",
            "oid": "reqseq",
            "reqseq": "0",
            "range": "bytes 0-{}/{}".format(length - 1, length),
            "tomid": to,
            "type": "video",
            "ver": "1.0"
        }
        headers = {
            "Content-Type": "video/mp4",
            "Content-Length": str(length),
            "x-obs-params": b64encode(json.dumps(params).encode()).decode()
        }
        headers.update(self.session._headers)
        url = f"https://{self.OBS}/r/talk/m/reqseq"
        result = await self.session.post(url, data=streamer(data=data),
                                         headers=headers)
        if result.status_code != 201:
            raise Exception("Failed to upload video.")

    async def sendVideoWithUrl(self, to, url):
        result = await self.session.get(url)
        await self.sendVideo(to, result)

    async def sendText(self, mid, text):
        return (await self.Talk.sendMessage(0, Message(to=mid, text=text)))

    async def sendProfileCover(self, to, mid):
        url = await self.Timeline.getProfileCoverURL(mid)
        result = await self.session.get(url)
        if result.status_code != 200:
            raise Exception("Failed to fetch profile image.")
        await self.sendImage(to, result)

    async def sendProfileImage(self, to, mid):
        url = f"http://{self.OBS}/os/p/{mid}"
        result = await self.session.get(url)
        if result.status_code != 200:
            raise Exception("Failed to fetch profile image.")
        await self.sendImage(to, result)

    async def sendProfileVideo(self, to, mid):
        url = f"http://{self.OBS}/os/p/{mid}/vp"
        result = await self.session.get(url)
        if result.status_code != 200:
            raise Exception("Failed to fetch profile image.")
        await self.sendVideo(to, result)

    async def sendGroupImage(self, to, mid):
        url = "http://dl.profile.line-cdn.net/{}".format(
            (await self.Talk.getGroupWithoutMembers(mid)).pictureStatus)
        result = await self.session.get(url)
        if result.status_code != 200:
            raise Exception("Failed to fetch profile image.")
        await self.sendImage(to, result)

    async def sendMessageViaApps(self, to, messages):
        try:
            if self.JunglePang.cc:
                await self.JunglePang.sendMessage(to, messages)
            else:
                bearer = await self.Tenor.issueBearer(to)
                await self.Tenor.share(bearer, messages)
        except Exception:
            raise
