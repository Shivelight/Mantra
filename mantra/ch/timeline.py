# -*- coding: utf-8 -*-
import time
from os.path import getsize
from base64 import b64encode
from multidict import CIMultiDict

from ..lib.aiohttp import ClientResponse
from ..constant import MYHOME_PATH, KEEP_PATH
from ..util import generateOid, streamer


class Timeline(object):

    def __init__(self, mantra):
        self.mantra = mantra
        self.token = None
        self.obsToken = None
        self.refreshToken = None
        self.channelAccessToken = None
        self.headers = CIMultiDict({
            # "Content-Type": "application/json",
            "X-Line-Mid": mantra.mid
        })
        self.OBS_URL = f"https://{mantra.OBS}"
        self.MYHOME_URL = f"https://{mantra.LEGY}{MYHOME_PATH}"
        self.KEEP_URL = f"https://{mantra.LEGY}{KEEP_PATH}/api/v24/keep"

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
        channelToken = await self.client.issueChannelToken("1341209950")
        self.token = channelToken.token
        self.obsToken = channelToken.obsToken
        self.refreshToken = channelToken.refreshToken
        self.channelAccessToken = channelToken.channelAccessToken
        self.headers["X-Line-ChannelToken"] = self.channelAccessToken

    async def addImageToAlbum(self, mid, albumId, path):
        file = open(path, 'rb').read()
        rrange = len(file)
        params = {
            "oid": int(time.time()),
            "quality": "100",
            "range": "bytes 0-{}/{}".format(rrange - 1, rrange),
            "type": "image"
        }
        headers = {
            "Content-Type": "image/jpeg",
            "X-Line-Album": albumId,
            "x-obs-params": b64encode(str(params).encode()).decode()
        }
        url = self.OBS_URL + "/album/a/upload.nhn"
        result = await self.session.post(url, data=file, headers={
            **self.headers, **headers})

        if result.status_code != 201:
            raise Exception("Failed to upload image.")
        return await result.json()

    async def changeGroupAlbumName(self, mid, albumId, name):
        params = {
            "homeId": mid
        }
        data = {
            "title": name
        }
        url = self.MYHOME_URL + "/album/v3/album/" + albumId
        result = await self.session.request("PUT", url, params=params,
                                            json=data, headers=self.headers)
        if result.status_code != 201:
            raise Exception('Failed to change album name.')

    async def createComment(self, mid, postId, text):
        params = {
            "homeId": mid,
            "sourceType": "TIMELINE"
        }
        data = {
            "commentText": text,
            "activityExternalId": postId,
            "actorId": mid
        }
        url = self.MYHOME_URL + "/api/v39/comment/create.json"
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        return await result.json()

    async def createGroupAlbum(self, mid, name):
        params = {
            "homeId": mid,
            "count": "1",
            "auto": "0"
        }
        data = {
            "title": name,
            "type": "image"
        }
        url = self.MYHOME_URL + "/album/v3/album.json"
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        if result.status_code != 201:
            raise Exception('Failed to create a new album.')

    async def createGroupPost(self, mid, text):
        data = {
            "postInfo": {
                "readPermission": {
                    "homeId": mid
                }
            },
            "sourceType": "TIMELINE",
            "contents": {
                "text": text
            }
        }
        url = self.MYHOME_URL + "/api/v39/post/create.json"
        result = await self.session.result("POST", url, json=data,
                                           headers=self.headers)
        return await result.json()

    async def createPost(self, mid, text, holdingTime=None):
        params = {
            "homeId": mid,
            "sourceType": "TIMELINE"
        }
        data = {
            "postInfo": {
                "readPermission": {
                    "type": "ALL"
                }
            },
            "sourceType": "TIMELINE",
            "contents": {
                "text": text
            }
        }
        if holdingTime is not None:
            data["postInfo"]["holdingTime"] = holdingTime
        url = self.MYHOME_URL + "/api/v39/post/create.json"
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        return await result.json()

    async def deleteComment(self, mid, postId, commentId):
        params = {
            "homeId": mid,
            "sourceType": "TIMELINE"
        }
        data = {
            "commentId": commentId,
            "activityExternalId": postId,
            "actorId": mid
        }
        url = self.MYHOME_URL + "/api/v39/comment/delete.json",
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        return await result.json()

    async def deleteGroupAlbum(self, mid, albumId):
        params = {
            "homeId": mid
        }
        url = self.MYHOME_URL + "/album/v3/album/" + albumId,
        result = await self.session.request("DELETE", url, params=params,
                                            headers=self.headers)

        if result.status_code != 201:
            raise Exception('Delete album failure.')

    async def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1,
                      order='TIME'):
        assert order in {"NONE", "TIME", "RANKING"}
        params = {
            "postLimit": postLimit,
            "commentLimit": commentLimit,
            "likeLimit": likeLimit,
            "order": order
        }
        url = self.MYHOME_URL + "/api/v39/feed/list.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def getGroupAlbum(self, mid):
        params = {
            "homeId": mid,
            "type": "g",
            "sourceType": "TALKROOM"
        }
        url = self.MYHOME_URL + "/album/v3/albums.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def getGroupPost(self, mid, postLimit=10, commentLimit=1,
                           likeLimit=1):
        params = {
            "homeId": mid,
            "commentLimit": commentLimit,
            "likeLimit": likeLimit,
            "sourceType": "TALKROOM"
        }
        url = self.MYHOME_URL + "/api/v39/post/list.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1,
                             likeLimit=1):
        params = {
            'homeId': mid,
            'postLimit': postLimit,
            'commentLimit': commentLimit,
            'likeLimit': likeLimit,
            'sourceType': 'LINE_PROFILE_COVER'
        }
        url = self.MYHOME_URL + "/api/v39/post/list.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    # TODO
    async def getImageGroupAlbum(self, mid, albumId, objId, returnAs='path',
                                 saveAs=''):
        if saveAs == '':
            saveAs = self.genTempFile('path')
        if returnAs not in ['path', 'bool', 'bin']:
            raise Exception('Invalid returnAs value')
        hr = self.server.additionalHeaders(self.server.timelineHeaders, {
            'Content-Type': 'image/jpeg',
            'X-Line-Mid': mid,
            'X-Line-Album': albumId
        })
        params = {'ver': '1.0', 'oid': objId}
        url = self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/album/a/download.nhn', params)
        r = self.server.getContent(url, headers=hr)
        if r.status_code == 200:
            self.saveFile(saveAs, r.raw)
            if returnAs == 'path':
                return saveAs
            elif returnAs == 'bool':
                return True
            elif returnAs == 'bin':
                return r.raw
        else:
            raise Exception('Download image album failure.')

    async def getProfileCoverId(self, mid):
        profile = await self.getProfileDetail(mid)
        return profile['result']['objectId']

    async def getProfileCoverURL(self, mid):
        objectId = await self.getProfileCoverId(mid)
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" \
               + mid + "&oid=" + objectId

    async def getProfileDetail(self, mid):
        params = {
            "userMid": mid
        }
        url = self.MYHOME_URL + "/api/v1/userpopup/getDetail.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def likePost(self, mid, postId, likeType=1001):
        assert likeType in {1001, 1002, 1003, 1004, 1005, 1006}

        params = {
            "homeId": mid,
            "sourceType": "TIMELINE"
        }
        data = {
            "likeType": likeType,
            "activityExternalId": postId,
            "actorId": mid
        }
        url = self.MYHOME_URL + "/api/v39/like/create.json"
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        return await result.json()

    async def sendPostToTalk(self, mid, postId):
        params = {
            "receiveMid": mid,
            "postId": postId
        }
        url = self.MYHOME_URL + "/api/v39/post/sendPostToTalk.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def unlikePost(self, mid, postId):
        params = {
            "homeId": mid,
            "sourceType": "TIMELINE"
        }
        data = {
            "activityExternalId": postId,
            "actorId": mid
        }
        url = self.MYHOME_URL + "/api/v39/like/cancel.json"
        result = await self.session.request("POST", url, params=params,
                                            json=data, headers=self.headers)
        return await result.json()

    async def uploadProfileCover(self, obj, oid=None):
        if isinstance(obj, ClientResponse):
            length = int(obj.headers['Content-Length'])
            data = obj.content
        else:
            data = open(data, 'rb').read()
            length = len(data)
        oid = generateOid() if oid is None else oid
        params = {
            "name": "cover",
            "oid": oid,
            "range": f"bytes 0-{length - 1}/{length}",
            "type": "image",
            "userid": self.mid,
            "ver": "1.0",
        }
        headers = {
            'Content-Type': 'image/jpeg',
            'Content-Length': str(length),
            'x-obs-params': b64encode(str(params).encode()).decode()
        }
        headers.update(self.headers)
        url = f"{self.OBS_URL}/r/myhome/c/{oid}"
        result = await self.session.post(url, data=streamer(data=data),
                                         headers=headers)
        if result.status_code != 201:
            raise Exception("Failed to upload cover.")
        return result.headers['x-obs-oid'], result.headers['x-obs-hash']

    async def updateProfileCoverByOid(self, objId):
        params = {
            "coverImageId": objId
        }
        url = f"{self.MYHOME_URL}/api/v39/home/updateCover.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def keepFetch(self, startRevision, endRevision, limit=50):
        params = {
            "startRevision": startRevision,
            "endRevision": endRevision,
            "limit": limit,
        }
        url = f"{self.KEEP_URL}/fetch.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def keepSync(self, revision, limit=50):
        params = {
            "revision": revision,
            "limit": limit,
        }
        url = f"{self.KEEP_URL}/sync.json"
        result = await self.session.get(url, params=params, headers=self.headers)
        return await result.json()

    async def keepSize(self):
        url = f"{self.KEEP_URL}/size.json"
        result = await self.session.get(url, headers=self.headers)
        return await result.json()

    async def keepDelete(self, contentId):
        data = {
            "contentId": contentId
        }
        url = f"{self.KEEP_URL}/delete.json"
        result = await self.session.post(url, json=data)
        return await result.json()

    async def keepDeleteBulk(self, contentIds):
        data = {
            "contentIds": contentIds
        }
        url = f"{self.KEEP_URL}/deleteBulk.json"
        result = await self.session.post(url, json=data)
        return await result.json()

    async def keepGet(self, contentId):
        params = {
            "contentId": contentId
        }
        url = f"{self.KEEP_URL}/get.json"
        result = await self.session.get(url, params=params)
        return await result.json()
