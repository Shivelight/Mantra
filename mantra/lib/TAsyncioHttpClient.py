# -*- coding: utf-8 -*-
from io import BytesIO
from urllib.parse import urlparse
from thrift.transport.TTransport import TTransportBase


class TAsyncioHttpClient(TTransportBase):

    def __init__(self, url, client):

        parsed = urlparse(url)

        assert parsed.scheme in ('http', 'https')

        self.scheme = parsed.scheme + "://"
        self.host = parsed.netloc
        self.path = parsed.path
        self._wbuf = BytesIO()
        self.client = client
        self.headers = client._headers
        self.custom_headers = {'Content-Type': 'application/x-thrift'}
        self.skip_headers = ['Accept', 'Accept-Encoding', 'User-Agent',
                             'Content-Type']

    @property
    def getHeaders(self):
        # try:
        #     return {'x-ls': self._resp.headers['x-ls'],
        #             'Content-Type': 'application/x-thrift'}
        # except Exception:
        return {**self.headers, **self.custom_headers}

    def close(self):
        self.client.close()

    def isOpen(self):
        return False if self.client.closed else True

    def setDefaultHeaders(self, headers):
        self.headers = headers

    def updateDefaultHeaders(self, headers):
        self.headers.update(headers)

    def setCustomHeaders(self, headers):
        self.custom_headers = headers

    def updateCustomHeaders(self, headers):
        self.custom_headers.update(headers)

    async def read(self, sz):
        return (await self._resp.content.read(sz))

    async def readAll(self, sz):
        buff = b''
        while sz:
            chunk = await self.read(sz)
            sz -= len(chunk)
            buff += chunk

            if len(chunk) == 0:
                raise EOFError

        return buff

    def write(self, buf):
        self._wbuf.write(buf)

    async def flush(self):

        data = self._wbuf.getvalue()
        self._wbuf = BytesIO()
        url = f"{self.scheme}{self.host}{self.path}"
        self._resp = await self.client.post(
            url, data=data, headers=self.getHeaders, ssl=False,
            skip_auto_headers=self.skip_headers)
