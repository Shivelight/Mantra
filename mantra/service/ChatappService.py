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

    async def getChatapp(self, request):
        """
        Parameters:
         - request
        """
        await self.send_getChatapp(request)
        return (await self.recv_getChatapp())

    async def send_getChatapp(self, request):
        self._oprot.writeMessageBegin('getChatapp', TMessageType.CALL, self._seqid)
        args = getChatapp_args()
        args.request = request
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_getChatapp(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = getChatapp_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "getChatapp failed: unknown result")

    async def getMyChatapps(self, request):
        """
        Parameters:
         - request
        """
        await self.send_getMyChatapps(request)
        return (await self.recv_getMyChatapps())

    async def send_getMyChatapps(self, request):
        self._oprot.writeMessageBegin('getMyChatapps', TMessageType.CALL, self._seqid)
        args = getMyChatapps_args()
        args.request = request
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_getMyChatapps(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = getMyChatapps_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "getMyChatapps failed: unknown result")

# HELPER FUNCTIONS AND STRUCTURES


class getChatapp_args(object):
    """
    Attributes:
     - request
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'request', (GetChatappRequest, GetChatappRequest.thrift_spec), None, ),  # 1
    )

    def __init__(self, request=None,):
        self.request = request

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetChatappRequest()
                    await self.request.read(iprot)
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
        oprot.writeStructBegin('getChatapp_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
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


class getChatapp_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (GetChatappResponse, GetChatappResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'e', (ChatappException, ChatappException.thrift_spec), None, ),  # 1
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
                    self.success = GetChatappResponse()
                    await self.success.read(iprot)
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = ChatappException()
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
        oprot.writeStructBegin('getChatapp_result')
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


class getMyChatapps_args(object):
    """
    Attributes:
     - request
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'request', (GetMyChatappsRequest, GetMyChatappsRequest.thrift_spec), None, ),  # 1
    )

    def __init__(self, request=None,):
        self.request = request

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.request = GetMyChatappsRequest()
                    await self.request.read(iprot)
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
        oprot.writeStructBegin('getMyChatapps_args')
        if self.request is not None:
            oprot.writeFieldBegin('request', TType.STRUCT, 1)
            self.request.write(oprot)
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


class getMyChatapps_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (GetMyChatappsResponse, GetMyChatappsResponse.thrift_spec), None, ),  # 0
        (1, TType.STRUCT, 'e', (ChatappException, ChatappException.thrift_spec), None, ),  # 1
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
                    self.success = GetMyChatappsResponse()
                    await self.success.read(iprot)
                else:
                    await iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.e = ChatappException()
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
        oprot.writeStructBegin('getMyChatapps_result')
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
