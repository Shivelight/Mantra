from io import BytesIO
import asyncio


def poll(transport, protocol):
    transport.suggested_amount = 1
    transport.throttle = 0.2
    # return
    # if protocol == "binary":
    #     p = "/P3"
    #     np = "/F3"
    # elif protocol == "compact":
    #     p = "/P4"
    #     np = "/NP4"

    async def flush(self):
        data = self._wbuf.getvalue()
        self._wbuf = BytesIO()
        url = f"{self.scheme}{self.host}{self.path}"
        self._resp = await self.client.post(
            url,
            data=data,
            headers=self.getHeaders,
            ssl=False,
            skip_auto_headers=self.skip_headers,
        )
        if self._resp.status == 204:
            await asyncio.sleep(self.throttle)
            # self.path = p
            # self.suggested_amount = 1
            # self.custom_headers = {"Connection": "close"}
        # elif self._resp.status == 200:
        #     self.path = np
        #     self.suggested_amount = 50
            # self.custom_headers = {"Connection": "keep-alive"}

    setattr(transport, "flush", flush.__get__(transport))
