#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import asyncio
from io import BytesIO
import logging
from struct import pack, unpack

from thrift.Thrift import TType, TApplicationException
from thrift.protocol.TBinaryProtocol import TBinaryProtocol, \
    TBinaryProtocolFactory
from thrift.protocol.TCompactProtocol import TCompactProtocol, \
    TCompactProtocolFactory, fromZigZag, reader, CLEAR, FIELD_READ, \
    CONTAINER_READ, VALUE_READ, BOOL_READ, CompactType
from thrift.protocol.TProtocol import TProtocolException
from thrift.transport import TTransport, TZlibTransport


class TAsyncioBaseTransport(TTransport.TTransportBase):

    async def readAll(self, sz):
        buff = b''
        while sz:
            chunk = await self.read(sz)
            sz -= len(chunk)
            buff += chunk

            if len(chunk) == 0:
                raise EOFError()

        return buff


class TAsyncioTransport(TAsyncioBaseTransport):
    """An abstract transport over asyncio streams"""
    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer
        self._wbuf = BytesIO()
        self._logger = logging.getLogger("TAsyncioTransport")

    @classmethod
    async def connect(cls, host, port, loop=None, ssl=False):
        reader, writer = await asyncio.open_connection(
            host, port, loop=loop, ssl=ssl)
        return cls(reader, writer)

    def write(self, buf):
        try:
            self._wbuf.write(buf)
        except Exception as e:
            # reset wbuf so it doesn't contain a partial function call
            self._wbuf.seek(0)
            raise e from None

    async def flush(self):
        wbuf = self._wbuf
        size = wbuf.tell()
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('writing %s of size %d: %s',
                               size, 'frame' if self.framed else "data",
                               wbuf.getvalue()[:size])
        data = self._get_flushed_data()
        self._writer.write(data)
        wbuf.seek(0)
        await self._writer.drain()

    def close(self):
        self._reader.feed_eof()
        self._writer.close()


class TAsyncioBufferedTransport(TAsyncioTransport):
    """A buffered transport over asyncio streams"""

    async def read(self, sz):
        return (await self._reader.read(sz))

    def _get_flushed_data(self):
        wbuf = self._wbuf
        size = wbuf.tell()
        if size < 1024:
            return wbuf.getvalue()[:size]
        return memoryview(wbuf.getvalue())[:size]


class TAsyncioFramedTransport(TAsyncioTransport):
    """A buffered transport over an asyncio stream"""
    def __init__(self, reader, writer):
        super(TAsyncioFramedTransport, self).__init__(reader, writer)
        self._rbuf = BytesIO()

    async def read(self, sz):
        ret = self._rbuf.read(sz)
        if ret:
            return ret
        await self.readFrame()
        return self._rbuf.read(sz)

    async def readFrame(self):
        buff = await self._reader.readexactly(4)
        sz, = unpack('!i', buff)
        self._rbuf = BytesIO((await self._reader.readexactly(sz)))

    def _get_flushed_data(self):
        wbuf = self._wbuf
        size = wbuf.tell()
        return pack("!i", size) + wbuf.getvalue()[:size]


class TAsyncioZlibTransport(TZlibTransport.TZlibTransport,
                            TAsyncioBaseTransport):
    """Class that wraps an asyncio-friendly transport with zlib, compressing
    writes and decompresses reads, using the python standard
    library zlib module.
    """

    async def read(self, sz):
        """Read up to sz bytes from the decompressed bytes buffer, and
        read from the underlying transport if the decompression
        buffer is empty.
        """
        ret = self._rbuf.read(sz)
        if len(ret) > 0:
            return ret
        # keep reading from transport until something comes back
        while True:
            if (await self.readComp(sz)):
                break
        ret = self._rbuf.read(sz)
        return ret

    async def readComp(self, sz):
        """Read compressed data from the underlying transport, then
        decompress it and append it to the internal StringIO read buffer
        """
        zbuf = await self._trans.read(sz)
        return self._readComp(zbuf)

    async def flush(self):
        """Flush any queued up data in the write buffer and ensure the
        compression buffer is flushed out to the underlying transport
        """
        super(TAsyncioZlibTransport, self).flush()
        # flush() in the base class is effectively a no-op
        await self._trans.flush()

    async def cstringio_refill(self, partialread, reqlen):
        """Implement the CReadableTransport interface for refill"""
        retstring = partialread
        if reqlen < self.DEFAULT_BUFFSIZE:
            retstring += await self.read(self.DEFAULT_BUFFSIZE)
        while len(retstring) < reqlen:
            retstring += await self.read(reqlen - len(retstring))
        self._rbuf = BytesIO(retstring)
        return self._rbuf


class TAsyncioBinaryProtocol(TBinaryProtocol):

    """Binary implementation of the Thrift protocol driver for asyncio."""

    _fast_encode = None
    _fast_decode = None

    async def readMessageBegin(self):
        sz = await self.readI32()
        if sz < 0:
            version = sz & TBinaryProtocol.VERSION_MASK
            if version != TBinaryProtocol.VERSION_1:
                raise TProtocolException(
                    type=TProtocolException.BAD_VERSION,
                    message='Bad version in readMessageBegin: %d' % (sz))
            type = sz & TBinaryProtocol.TYPE_MASK
            name = await self.readString()
            seqid = await self.readI32()
        else:
            if self.strictRead:
                raise TProtocolException(type=TProtocolException.BAD_VERSION,
                                         message='No protocol version header')
            name = await self.trans.readAll(sz)
            type = await self.readByte()
            seqid = await self.readI32()
        return (name, type, seqid)

    async def readMessageEnd(self):
        pass

    async def readStructBegin(self):
        pass

    async def readStructEnd(self):
        pass

    async def readFieldBegin(self):
        type = await self.readByte()
        if type == TType.STOP:
            return (None, type, 0)
        id = await self.readI16()
        return (None, type, id)

    async def readFieldEnd(self):
        pass

    async def readMapBegin(self):
        ktype = await self.readByte()
        vtype = await self.readByte()
        size = await self.readI32()
        self._check_container_length(size)
        return (ktype, vtype, size)

    async def readMapEnd(self):
        pass

    async def readListBegin(self):
        etype = await self.readByte()
        size = await self.readI32()
        self._check_container_length(size)
        return (etype, size)

    async def readListEnd(self):
        pass

    async def readSetBegin(self):
        etype = await self.readByte()
        size = await self.readI32()
        self._check_container_length(size)
        return (etype, size)

    async def readSetEnd(self):
        pass

    async def readBool(self):
        byte = await self.readByte()
        if byte == 0:
            return False
        return True

    async def readByte(self):
        buff = await self.trans.readAll(1)
        val, = unpack('!b', buff)
        return val

    async def readI16(self):
        buff = await self.trans.readAll(2)
        val, = unpack('!h', buff)
        return val

    async def readI32(self):
        buff = await self.trans.readAll(4)
        val, = unpack('!i', buff)
        return val

    async def readI64(self):
        buff = await self.trans.readAll(8)
        val, = unpack('!q', buff)
        return val

    async def readDouble(self):
        buff = await self.trans.readAll(8)
        val, = unpack('!d', buff)
        return val

    async def readBinary(self):
        size = await self.readI32()
        self._check_string_length(size)
        s = await self.trans.readAll(size)
        return s

    async def readString(self):
        return (await self.readBinary()).decode("utf-8")

    async def skip(self, type):
        if type == TType.STOP:
            return
        elif type == TType.BOOL:
            await self.readBool()
        elif type == TType.BYTE:
            await self.readByte()
        elif type == TType.I16:
            await self.readI16()
        elif type == TType.I32:
            await self.readI32()
        elif type == TType.I64:
            await self.readI64()
        elif type == TType.DOUBLE:
            await self.readDouble()
        elif type == TType.STRING:
            await self.readString()
        elif type == TType.STRUCT:
            name = await self.readStructBegin()
            while True:
                (name, type, id) = await self.readFieldBegin()
                if type == TType.STOP:
                    break
                await self.skip(type)
                await self.readFieldEnd()
            await self.readStructEnd()
        elif type == TType.MAP:
            (ktype, vtype, size) = await self.readMapBegin()
            for _ in range(size):
                await self.skip(ktype)
                await self.skip(vtype)
            await self.readMapEnd()
        elif type == TType.SET:
            (etype, size) = await self.readSetBegin()
            for _ in range(size):
                await self.skip(etype)
            await self.readSetEnd()
        elif type == TType.LIST:
            (etype, size) = await self.readListBegin()
            for _ in range(size):
                await self.skip(etype)
            await self.readListEnd()


class TAsyncioBinaryProtocolFactory(TBinaryProtocolFactory):
    def getProtocol(self, trans):
        return TAsyncioBinaryProtocol(trans, self.strictRead, self.strictWrite)


class TAsyncioCompactProtocol(TCompactProtocol):
    """Compact implementation of the Thrift protocol driver with asyncio."""

    async def readString(self):
        return (await self.readBinary()).decode("utf-8")

    async def readFieldBegin(self):
        assert self.state == FIELD_READ, self.state
        type = await self.__readUByte()
        if type & 0x0f == TType.STOP:
            return (None, 0, 0)
        delta = type >> 4
        if delta == 0:
            fid = await self.__readI16()
        else:
            fid = self._last_fid + delta
        self._last_fid = fid
        type = type & 0x0f
        if type == CompactType.TRUE:
            self.state = BOOL_READ
            self._bool_value = True
        elif type == CompactType.FALSE:
            self.state = BOOL_READ
            self._bool_value = False
        else:
            self.state = VALUE_READ
        return (None, self._getTType(type), fid)

    async def readFieldEnd(self):
        super(TAsyncioCompactProtocol, self).readFieldEnd()

    async def __readUByte(self):
        result, = unpack('!B', (await self.trans.readAll(1)))
        return result

    async def __readByte(self):
        result, = unpack('!b', (await self.trans.readAll(1)))
        return result

    async def __readVarint(self):
        result = 0
        shift = 0
        while True:
            x = await self.trans.readAll(1)
            byte = ord(x)
            result |= (byte & 0x7f) << shift
            if byte >> 7 == 0:
                return result
            shift += 7

    async def __readZigZag(self):
        return fromZigZag((await self.__readVarint()))

    async def __readSize(self):
        result = await self.__readVarint()
        if result < 0:
            raise TProtocolException("Length < 0")
        return result

    async def readMessageBegin(self):
        assert self.state == CLEAR
        proto_id = await self.__readUByte()
        if proto_id != self.PROTOCOL_ID:
            raise TProtocolException(TProtocolException.BAD_VERSION,
                                     'Bad protocol id in the message: %d' % proto_id)
        ver_type = await self.__readUByte()
        type = (ver_type >> self.TYPE_SHIFT_AMOUNT) & self.TYPE_BITS
        version = ver_type & self.VERSION_MASK
        if version != self.VERSION:
            raise TProtocolException(TProtocolException.BAD_VERSION,
                                     'Bad version: %d (expect %d)' % (version, self.VERSION))
        seqid = await self.__readVarint()
        name = (await self.__readBinary()).decode("utf-8")
        return (name, type, seqid)

    async def readMessageEnd(self):
        super(TAsyncioCompactProtocol, self).readMessageEnd()

    async def readStructBegin(self):
        super(TAsyncioCompactProtocol, self).readStructBegin()

    async def readStructEnd(self):
        super(TAsyncioCompactProtocol, self).readStructEnd()

    async def readCollectionBegin(self):
        assert self.state in (VALUE_READ, CONTAINER_READ), self.state
        size_type = await self.__readUByte()
        size = size_type >> 4
        type = self._getTType(size_type)
        if size == 15:
            size = await self.__readSize()
        self._check_container_length(size)
        self._containers.append(self.state)
        self.state = CONTAINER_READ
        return type, size

    readSetBegin = readCollectionBegin
    readListBegin = readCollectionBegin

    async def readMapBegin(self):
        assert self.state in (VALUE_READ, CONTAINER_READ), self.state
        size = await self.__readSize()
        self._check_container_length(size)
        types = 0
        if size > 0:
            types = await self.__readUByte()
        vtype = self._getTType(types)
        ktype = self._getTType(types >> 4)
        self._containers.append(self.state)
        self.state = CONTAINER_READ
        return (ktype, vtype, size)

    async def readCollectionEnd(self):
        super(TAsyncioCompactProtocol, self).readCollectionEnd()

    readSetEnd = readCollectionEnd
    readListEnd = readCollectionEnd
    readMapEnd = readCollectionEnd

    async def readBool(self):
        return super(TAsyncioCompactProtocol, self).readBool()

    readByte = reader(__readByte)
    __readI16 = __readZigZag
    readI16 = reader(__readZigZag)
    readI32 = reader(__readZigZag)
    readI64 = reader(__readZigZag)

    @reader
    async def readDouble(self):
        buff = await self.trans.readAll(8)
        val, = unpack('<d', buff)
        return val

    async def __readBinary(self):
        size = await self.__readSize()
        self._check_string_length(size)
        return (await self.trans.readAll(size))
    readBinary = reader(__readBinary)

    async def skip(self, type):
        if type == TType.STOP:
            return
        elif type == TType.BOOL:
            await self.readBool()
        elif type == TType.BYTE:
            await self.readByte()
        elif type == TType.I16:
            await self.readI16()
        elif type == TType.I32:
            await self.readI32()
        elif type == TType.I64:
            await self.readI64()
        elif type == TType.DOUBLE:
            await self.readDouble()
        elif type == TType.STRING:
            await self.readString()
        elif type == TType.STRUCT:
            name = await self.readStructBegin()
            while True:
                (name, type, id) = await self.readFieldBegin()
                if type == TType.STOP:
                    break
                await self.skip(type)
                await self.readFieldEnd()
            await self.readStructEnd()
        elif type == TType.MAP:
            (ktype, vtype, size) = await self.readMapBegin()
            for _ in range(size):
                await self.skip(ktype)
                await self.skip(vtype)
            await self.readMapEnd()
        elif type == TType.SET:
            (etype, size) = await self.readSetBegin()
            for _ in range(size):
                await self.skip(etype)
            await self.readSetEnd()
        elif type == TType.LIST:
            (etype, size) = await self.readListBegin()
            for _ in range(size):
                await self.skip(etype)
            await self.readListEnd()


class TAsyncioCompactProtocolFactory(TCompactProtocolFactory):
    def getProtocol(self, trans):
        return TAsyncioCompactProtocol(trans,
                                       self.string_length_limit,
                                       self.container_length_limit)


class TAsyncioApplicationException(TApplicationException):
    async def read(self, iprot):
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    message = await iprot.readString()
                    if isinstance(message, bytes):
                        try:
                            message = message.decode('utf-8')
                        except UnicodeDecodeError:
                            pass
                    self.message = message
                else:
                    await iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.type = await iprot.readI32()
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()
