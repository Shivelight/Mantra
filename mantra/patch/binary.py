from struct import pack


def talk(client):
    async def sendText(self, to, text):
        payload = (
            b"\x80\x01\x00\x01\x00\x00\x00\x0bsendMessage\x00\x00\x00\x00\x08"
            b"\x00\x01\x00\x00\x00\x00\x0c\x00\x02\x0b\x00\x02\x00\x00\x00!"
        )
        self._oprot.trans.write(payload)
        text = text.encode('utf-8')
        self._oprot.trans.write(to.encode())
        self._oprot.trans.write(b"\x0b\x00\n")
        self._oprot.trans.write(pack('!i', len(text)))
        self._oprot.trans.write(text)
        self._oprot.trans.write(b"\x00\x00")

        # self._oprot.trans.write(
        #     to.encode() + b"\x0b\x00\n" + pack('!i', len(text)) +
        #     text.encode() + b"\x00\x00"
        # )
        await self._oprot.trans.flush()

    async def kickoutFromGroup(self, reqSeq, groupId, contactIds):
        await self.send_kickoutFromGroup(reqSeq, groupId, contactIds)

    for name, func in locals().items():
        if callable(func):
            setattr(client, name, func.__get__(client))
