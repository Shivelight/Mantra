#
# Autogenerated by Thrift Compiler ()
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:asyncio
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException
from thrift.protocol.TProtocol import TProtocolException
import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.TAsyncio import TAsyncioApplicationException


class Client(object):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    async def fetchMessageOperations(self, localRevision, lastOpTimestamp, count):
        """
        Parameters:
         - localRevision
         - lastOpTimestamp
         - count
        """
        await self.send_fetchMessageOperations(localRevision, lastOpTimestamp, count)
        return (await self.recv_fetchMessageOperations())

    async def send_fetchMessageOperations(self, localRevision, lastOpTimestamp, count):
        self._oprot.writeMessageBegin('fetchMessageOperations', TMessageType.CALL, self._seqid)
        args = fetchMessageOperations_args()
        args.localRevision = localRevision
        args.lastOpTimestamp = lastOpTimestamp
        args.count = count
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_fetchMessageOperations(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = fetchMessageOperations_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "fetchMessageOperations failed: unknown result")

    async def getLastReadMessageIds(self, chatId):
        """
        Parameters:
         - chatId
        """
        await self.send_getLastReadMessageIds(chatId)
        return (await self.recv_getLastReadMessageIds())

    async def send_getLastReadMessageIds(self, chatId):
        self._oprot.writeMessageBegin('getLastReadMessageIds', TMessageType.CALL, self._seqid)
        args = getLastReadMessageIds_args()
        args.chatId = chatId
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_getLastReadMessageIds(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = getLastReadMessageIds_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "getLastReadMessageIds failed: unknown result")

    async def multiGetLastReadMessageIds(self, chatIds):
        """
        Parameters:
         - chatIds
        """
        await self.send_multiGetLastReadMessageIds(chatIds)
        return (await self.recv_multiGetLastReadMessageIds())

    async def send_multiGetLastReadMessageIds(self, chatIds):
        self._oprot.writeMessageBegin('multiGetLastReadMessageIds', TMessageType.CALL, self._seqid)
        args = multiGetLastReadMessageIds_args()
        args.chatIds = chatIds
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_multiGetLastReadMessageIds(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = multiGetLastReadMessageIds_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "multiGetLastReadMessageIds failed: unknown result")

# HELPER FUNCTIONS AND STRUCTURES


class fetchMessageOperations_args(object):
    """
    Attributes:
     - localRevision
     - lastOpTimestamp
     - count
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.I64, 'localRevision', None, None, ),  # 2
        (3, TType.I64, 'lastOpTimestamp', None, None, ),  # 3
        (4, TType.I32, 'count', None, None, ),  # 4
    )

    def __init__(self, localRevision=None, lastOpTimestamp=None, count=None,):
        self.localRevision = localRevision
        self.lastOpTimestamp = lastOpTimestamp
        self.count = count

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.I64:
                    self.localRevision = await iprot.readI64()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.lastOpTimestamp = await iprot.readI64()
                else:
                    await iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.count = await iprot.readI32()
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('fetchMessageOperations_args')
        if self.localRevision is not None:
            oprot.writeFieldBegin('localRevision', TType.I64, 2)
            oprot.writeI64(self.localRevision)
            oprot.writeFieldEnd()
        if self.lastOpTimestamp is not None:
            oprot.writeFieldBegin('lastOpTimestamp', TType.I64, 3)
            oprot.writeI64(self.lastOpTimestamp)
            oprot.writeFieldEnd()
        if self.count is not None:
            oprot.writeFieldBegin('count', TType.I32, 4)
            oprot.writeI32(self.count)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class fetchMessageOperations_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (MessageOperations, MessageOperations.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = MessageOperations()
                    await self.success.read(iprot)
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = TalkException()
                    await self.e.read(iprot)
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('fetchMessageOperations_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class getLastReadMessageIds_args(object):
    """
    Attributes:
     - chatId
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.STRING, 'chatId', 'UTF8', None, ),  # 2
    )

    def __init__(self, chatId=None,):
        self.chatId = chatId

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.STRING:
                    self.chatId = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('getLastReadMessageIds_args')
        if self.chatId is not None:
            oprot.writeFieldBegin('chatId', TType.STRING, 2)
            oprot.writeString(self.chatId)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class getLastReadMessageIds_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (LastReadMessageIds, LastReadMessageIds.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = LastReadMessageIds()
                    await self.success.read(iprot)
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = TalkException()
                    await self.e.read(iprot)
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('getLastReadMessageIds_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class multiGetLastReadMessageIds_args(object):
    """
    Attributes:
     - chatIds
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.LIST, 'chatIds', (TType.STRING, 'UTF8', False), None, ),  # 2
    )

    def __init__(self, chatIds=None,):
        self.chatIds = chatIds

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 2:
                if ftype == TType.LIST:
                    self.chatIds = []
                    (_etype1830, _size1827) = await iprot.readListBegin()
                    for _i1831 in range(_size1827):
                        _elem1832 = await iprot.readString()
                        self.chatIds.append(_elem1832)
                    await iprot.readListEnd()
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('multiGetLastReadMessageIds_args')
        if self.chatIds is not None:
            oprot.writeFieldBegin('chatIds', TType.LIST, 2)
            oprot.writeListBegin(TType.STRING, len(self.chatIds))
            for iter1833 in self.chatIds:
                oprot.writeString(iter1833)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class multiGetLastReadMessageIds_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.LIST, 'success', (TType.STRUCT, (LastReadMessageIds, LastReadMessageIds.thrift_spec), False), None, ),  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, success=None, e=None,):
        self.success = success
        self.e = e

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    (_etype1837, _size1834) = await iprot.readListBegin()
                    for _i1838 in range(_size1834):
                        _elem1839 = LastReadMessageIds()
                        await _elem1839.read(iprot)
                        self.success.append(_elem1839)
                    await iprot.readListEnd()
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = TalkException()
                    await self.e.read(iprot)
                else:
                    await iprot.skip(ftype)
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('multiGetLastReadMessageIds_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter1840 in self.success:
                iter1840.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
