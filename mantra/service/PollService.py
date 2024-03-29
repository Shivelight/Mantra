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

    async def fetchOperations(self, localRev, count):
        """
        Parameters:
         - localRev
         - count
        """
        await self.send_fetchOperations(localRev, count)
        return (await self.recv_fetchOperations())

    async def send_fetchOperations(self, localRev, count):
        self._oprot.writeMessageBegin('fetchOperations', TMessageType.CALL, self._seqid)
        args = fetchOperations_args()
        args.localRev = localRev
        args.count = count
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_fetchOperations(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = fetchOperations_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "fetchOperations failed: unknown result")

    async def fetchOps(self, localRev, count, globalRev, individualRev):
        """
        Parameters:
         - localRev
         - count
         - globalRev
         - individualRev
        """
        await self.send_fetchOps(localRev, count, globalRev, individualRev)
        return (await self.recv_fetchOps())

    async def send_fetchOps(self, localRev, count, globalRev, individualRev):
        self._oprot.writeMessageBegin('fetchOps', TMessageType.CALL, self._seqid)
        args = fetchOps_args()
        args.localRev = localRev
        args.count = count
        args.globalRev = globalRev
        args.individualRev = individualRev
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_fetchOps(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = fetchOps_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        if result.s is not None:
            raise result.s
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "fetchOps failed: unknown result")

# HELPER FUNCTIONS AND STRUCTURES


class fetchOperations_args(object):
    """
    Attributes:
     - localRev
     - count
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.I64, 'localRev', None, None, ),  # 2
        (3, TType.I32, 'count', None, None, ),  # 3
    )

    def __init__(self, localRev=None, count=None,):
        self.localRev = localRev
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
                    self.localRev = await iprot.readI64()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
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
        oprot.writeStructBegin('fetchOperations_args')
        if self.localRev is not None:
            oprot.writeFieldBegin('localRev', TType.I64, 2)
            oprot.writeI64(self.localRev)
            oprot.writeFieldEnd()
        if self.count is not None:
            oprot.writeFieldBegin('count', TType.I32, 3)
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


class fetchOperations_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.LIST, 'success', (TType.STRUCT, (Operation, Operation.thrift_spec), False), None, ),  # 0
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
                    (_etype1872, _size1869) = await iprot.readListBegin()
                    for _i1873 in range(_size1869):
                        _elem1874 = Operation()
                        await _elem1874.read(iprot)
                        self.success.append(_elem1874)
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
        oprot.writeStructBegin('fetchOperations_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter1875 in self.success:
                iter1875.write(oprot)
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


class fetchOps_args(object):
    """
    Attributes:
     - localRev
     - count
     - globalRev
     - individualRev
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.I64, 'localRev', None, None, ),  # 2
        (3, TType.I32, 'count', None, None, ),  # 3
        (4, TType.I64, 'globalRev', None, None, ),  # 4
        (5, TType.I64, 'individualRev', None, None, ),  # 5
    )

    def __init__(self, localRev=None, count=None, globalRev=None, individualRev=None,):
        self.localRev = localRev
        self.count = count
        self.globalRev = globalRev
        self.individualRev = individualRev

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
                    self.localRev = await iprot.readI64()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.count = await iprot.readI32()
                else:
                    await iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I64:
                    self.globalRev = await iprot.readI64()
                else:
                    await iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I64:
                    self.individualRev = await iprot.readI64()
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
        oprot.writeStructBegin('fetchOps_args')
        if self.localRev is not None:
            oprot.writeFieldBegin('localRev', TType.I64, 2)
            oprot.writeI64(self.localRev)
            oprot.writeFieldEnd()
        if self.count is not None:
            oprot.writeFieldBegin('count', TType.I32, 3)
            oprot.writeI32(self.count)
            oprot.writeFieldEnd()
        if self.globalRev is not None:
            oprot.writeFieldBegin('globalRev', TType.I64, 4)
            oprot.writeI64(self.globalRev)
            oprot.writeFieldEnd()
        if self.individualRev is not None:
            oprot.writeFieldBegin('individualRev', TType.I64, 5)
            oprot.writeI64(self.individualRev)
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


class fetchOps_result(object):
    """
    Attributes:
     - success
     - e
     - s
    """

    thrift_spec = (
        (0, TType.LIST, 'success', (TType.STRUCT, (Operation, Operation.thrift_spec), False), None, ),  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
        (2, TType.STRUCT, 's', (ShouldSyncException, ShouldSyncException.thrift_spec), None, ),  # 2
    )

    def __init__(self, success=None, e=None, s=None,):
        self.success = success
        self.e = e
        self.s = s

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
                    (_etype1879, _size1876) = await iprot.readListBegin()
                    for _i1880 in range(_size1876):
                        _elem1881 = Operation()
                        await _elem1881.read(iprot)
                        self.success.append(_elem1881)
                    await iprot.readListEnd()
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = TalkException()
                    await self.e.read(iprot)
                else:
                    await iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.s = ShouldSyncException()
                    await self.s.read(iprot)
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
        oprot.writeStructBegin('fetchOps_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter1882 in self.success:
                iter1882.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.e is not None:
            oprot.writeFieldBegin('e', TType.STRUCT, 1)
            self.e.write(oprot)
            oprot.writeFieldEnd()
        if self.s is not None:
            oprot.writeFieldBegin('s', TType.STRUCT, 2)
            self.s.write(oprot)
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
