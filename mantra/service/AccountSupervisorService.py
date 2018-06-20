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

    async def getRSAKey(self):
        await self.send_getRSAKey()
        return (await self.recv_getRSAKey())

    async def send_getRSAKey(self):
        self._oprot.writeMessageBegin('getRSAKey', TMessageType.CALL, self._seqid)
        args = getRSAKey_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_getRSAKey(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = getRSAKey_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "getRSAKey failed: unknown result")

    async def notifyEmailConfirmationResult(self, parameterMap):
        """
        Parameters:
         - parameterMap
        """
        await self.send_notifyEmailConfirmationResult(parameterMap)
        (await self.recv_notifyEmailConfirmationResult())

    async def send_notifyEmailConfirmationResult(self, parameterMap):
        self._oprot.writeMessageBegin('notifyEmailConfirmationResult', TMessageType.CALL, self._seqid)
        args = notifyEmailConfirmationResult_args()
        args.parameterMap = parameterMap
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_notifyEmailConfirmationResult(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = notifyEmailConfirmationResult_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    async def registerVirtualAccount(self, locale, encryptedVirtualUserId, encryptedPassword):
        """
        Parameters:
         - locale
         - encryptedVirtualUserId
         - encryptedPassword
        """
        await self.send_registerVirtualAccount(locale, encryptedVirtualUserId, encryptedPassword)
        return (await self.recv_registerVirtualAccount())

    async def send_registerVirtualAccount(self, locale, encryptedVirtualUserId, encryptedPassword):
        self._oprot.writeMessageBegin('registerVirtualAccount', TMessageType.CALL, self._seqid)
        args = registerVirtualAccount_args()
        args.locale = locale
        args.encryptedVirtualUserId = encryptedVirtualUserId
        args.encryptedPassword = encryptedPassword
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_registerVirtualAccount(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = registerVirtualAccount_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.e is not None:
            raise result.e
        raise TAsyncioApplicationException(TAsyncioApplicationException.MISSING_RESULT, "registerVirtualAccount failed: unknown result")

    async def requestVirtualAccountPasswordChange(self, virtualMid, encryptedVirtualUserId, encryptedOldPassword, encryptedNewPassword):
        """
        Parameters:
         - virtualMid
         - encryptedVirtualUserId
         - encryptedOldPassword
         - encryptedNewPassword
        """
        await self.send_requestVirtualAccountPasswordChange(virtualMid, encryptedVirtualUserId, encryptedOldPassword, encryptedNewPassword)
        (await self.recv_requestVirtualAccountPasswordChange())

    async def send_requestVirtualAccountPasswordChange(self, virtualMid, encryptedVirtualUserId, encryptedOldPassword, encryptedNewPassword):
        self._oprot.writeMessageBegin('requestVirtualAccountPasswordChange', TMessageType.CALL, self._seqid)
        args = requestVirtualAccountPasswordChange_args()
        args.virtualMid = virtualMid
        args.encryptedVirtualUserId = encryptedVirtualUserId
        args.encryptedOldPassword = encryptedOldPassword
        args.encryptedNewPassword = encryptedNewPassword
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_requestVirtualAccountPasswordChange(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = requestVirtualAccountPasswordChange_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    async def requestVirtualAccountPasswordSet(self, virtualMid, encryptedVirtualUserId, encryptedNewPassword):
        """
        Parameters:
         - virtualMid
         - encryptedVirtualUserId
         - encryptedNewPassword
        """
        await self.send_requestVirtualAccountPasswordSet(virtualMid, encryptedVirtualUserId, encryptedNewPassword)
        (await self.recv_requestVirtualAccountPasswordSet())

    async def send_requestVirtualAccountPasswordSet(self, virtualMid, encryptedVirtualUserId, encryptedNewPassword):
        self._oprot.writeMessageBegin('requestVirtualAccountPasswordSet', TMessageType.CALL, self._seqid)
        args = requestVirtualAccountPasswordSet_args()
        args.virtualMid = virtualMid
        args.encryptedVirtualUserId = encryptedVirtualUserId
        args.encryptedNewPassword = encryptedNewPassword
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_requestVirtualAccountPasswordSet(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = requestVirtualAccountPasswordSet_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    async def unregisterVirtualAccount(self, virtualMid):
        """
        Parameters:
         - virtualMid
        """
        await self.send_unregisterVirtualAccount(virtualMid)
        (await self.recv_unregisterVirtualAccount())

    async def send_unregisterVirtualAccount(self, virtualMid):
        self._oprot.writeMessageBegin('unregisterVirtualAccount', TMessageType.CALL, self._seqid)
        args = unregisterVirtualAccount_args()
        args.virtualMid = virtualMid
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        await self._oprot.trans.flush()

    async def recv_unregisterVirtualAccount(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = await iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TAsyncioApplicationException()
            await x.read(iprot)
            await iprot.readMessageEnd()
            raise x
        result = unregisterVirtualAccount_result()
        await result.read(iprot)
        await iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

# HELPER FUNCTIONS AND STRUCTURES


class getRSAKey_args(object):

    thrift_spec = (
    )

    async def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        await iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = await iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                await iprot.skip(ftype)
            await iprot.readFieldEnd()
        await iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('getRSAKey_args')
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


class getRSAKey_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRUCT, 'success', (RSAKey, RSAKey.thrift_spec), None, ),  # 0
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
                    self.success = RSAKey()
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
        oprot.writeStructBegin('getRSAKey_result')
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


class notifyEmailConfirmationResult_args(object):
    """
    Attributes:
     - parameterMap
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.MAP, 'parameterMap', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 2
    )

    def __init__(self, parameterMap=None,):
        self.parameterMap = parameterMap

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
                if ftype == TType.MAP:
                    self.parameterMap = {}
                    (_ktype1179, _vtype1180, _size1178) = await iprot.readMapBegin()
                    for _i1182 in range(_size1178):
                        _key1183 = await iprot.readString()
                        _val1184 = await iprot.readString()
                        self.parameterMap[_key1183] = _val1184
                    await iprot.readMapEnd()
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
        oprot.writeStructBegin('notifyEmailConfirmationResult_args')
        if self.parameterMap is not None:
            oprot.writeFieldBegin('parameterMap', TType.MAP, 2)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.parameterMap))
            for kiter1185, viter1186 in self.parameterMap.items():
                oprot.writeString(kiter1185)
                oprot.writeString(viter1186)
            oprot.writeMapEnd()
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


class notifyEmailConfirmationResult_result(object):
    """
    Attributes:
     - e
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, e=None,):
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
            if fid == 1:
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
        oprot.writeStructBegin('notifyEmailConfirmationResult_result')
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


class registerVirtualAccount_args(object):
    """
    Attributes:
     - locale
     - encryptedVirtualUserId
     - encryptedPassword
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.STRING, 'locale', 'UTF8', None, ),  # 2
        (3, TType.STRING, 'encryptedVirtualUserId', 'UTF8', None, ),  # 3
        (4, TType.STRING, 'encryptedPassword', 'UTF8', None, ),  # 4
    )

    def __init__(self, locale=None, encryptedVirtualUserId=None, encryptedPassword=None,):
        self.locale = locale
        self.encryptedVirtualUserId = encryptedVirtualUserId
        self.encryptedPassword = encryptedPassword

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
                    self.locale = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.encryptedVirtualUserId = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.encryptedPassword = await iprot.readString()
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
        oprot.writeStructBegin('registerVirtualAccount_args')
        if self.locale is not None:
            oprot.writeFieldBegin('locale', TType.STRING, 2)
            oprot.writeString(self.locale)
            oprot.writeFieldEnd()
        if self.encryptedVirtualUserId is not None:
            oprot.writeFieldBegin('encryptedVirtualUserId', TType.STRING, 3)
            oprot.writeString(self.encryptedVirtualUserId)
            oprot.writeFieldEnd()
        if self.encryptedPassword is not None:
            oprot.writeFieldBegin('encryptedPassword', TType.STRING, 4)
            oprot.writeString(self.encryptedPassword)
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


class registerVirtualAccount_result(object):
    """
    Attributes:
     - success
     - e
    """

    thrift_spec = (
        (0, TType.STRING, 'success', 'UTF8', None, ),  # 0
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
                if ftype == TType.STRING:
                    self.success = await iprot.readString()
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
        oprot.writeStructBegin('registerVirtualAccount_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRING, 0)
            oprot.writeString(self.success)
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


class requestVirtualAccountPasswordChange_args(object):
    """
    Attributes:
     - virtualMid
     - encryptedVirtualUserId
     - encryptedOldPassword
     - encryptedNewPassword
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.STRING, 'virtualMid', 'UTF8', None, ),  # 2
        (3, TType.STRING, 'encryptedVirtualUserId', 'UTF8', None, ),  # 3
        (4, TType.STRING, 'encryptedOldPassword', 'UTF8', None, ),  # 4
        (5, TType.STRING, 'encryptedNewPassword', 'UTF8', None, ),  # 5
    )

    def __init__(self, virtualMid=None, encryptedVirtualUserId=None, encryptedOldPassword=None, encryptedNewPassword=None,):
        self.virtualMid = virtualMid
        self.encryptedVirtualUserId = encryptedVirtualUserId
        self.encryptedOldPassword = encryptedOldPassword
        self.encryptedNewPassword = encryptedNewPassword

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
                    self.virtualMid = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.encryptedVirtualUserId = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.encryptedOldPassword = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.encryptedNewPassword = await iprot.readString()
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
        oprot.writeStructBegin('requestVirtualAccountPasswordChange_args')
        if self.virtualMid is not None:
            oprot.writeFieldBegin('virtualMid', TType.STRING, 2)
            oprot.writeString(self.virtualMid)
            oprot.writeFieldEnd()
        if self.encryptedVirtualUserId is not None:
            oprot.writeFieldBegin('encryptedVirtualUserId', TType.STRING, 3)
            oprot.writeString(self.encryptedVirtualUserId)
            oprot.writeFieldEnd()
        if self.encryptedOldPassword is not None:
            oprot.writeFieldBegin('encryptedOldPassword', TType.STRING, 4)
            oprot.writeString(self.encryptedOldPassword)
            oprot.writeFieldEnd()
        if self.encryptedNewPassword is not None:
            oprot.writeFieldBegin('encryptedNewPassword', TType.STRING, 5)
            oprot.writeString(self.encryptedNewPassword)
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


class requestVirtualAccountPasswordChange_result(object):
    """
    Attributes:
     - e
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, e=None,):
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
            if fid == 1:
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
        oprot.writeStructBegin('requestVirtualAccountPasswordChange_result')
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


class requestVirtualAccountPasswordSet_args(object):
    """
    Attributes:
     - virtualMid
     - encryptedVirtualUserId
     - encryptedNewPassword
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.STRING, 'virtualMid', 'UTF8', None, ),  # 2
        (3, TType.STRING, 'encryptedVirtualUserId', 'UTF8', None, ),  # 3
        (4, TType.STRING, 'encryptedNewPassword', 'UTF8', None, ),  # 4
    )

    def __init__(self, virtualMid=None, encryptedVirtualUserId=None, encryptedNewPassword=None,):
        self.virtualMid = virtualMid
        self.encryptedVirtualUserId = encryptedVirtualUserId
        self.encryptedNewPassword = encryptedNewPassword

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
                    self.virtualMid = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.encryptedVirtualUserId = await iprot.readString()
                else:
                    await iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.encryptedNewPassword = await iprot.readString()
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
        oprot.writeStructBegin('requestVirtualAccountPasswordSet_args')
        if self.virtualMid is not None:
            oprot.writeFieldBegin('virtualMid', TType.STRING, 2)
            oprot.writeString(self.virtualMid)
            oprot.writeFieldEnd()
        if self.encryptedVirtualUserId is not None:
            oprot.writeFieldBegin('encryptedVirtualUserId', TType.STRING, 3)
            oprot.writeString(self.encryptedVirtualUserId)
            oprot.writeFieldEnd()
        if self.encryptedNewPassword is not None:
            oprot.writeFieldBegin('encryptedNewPassword', TType.STRING, 4)
            oprot.writeString(self.encryptedNewPassword)
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


class requestVirtualAccountPasswordSet_result(object):
    """
    Attributes:
     - e
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, e=None,):
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
            if fid == 1:
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
        oprot.writeStructBegin('requestVirtualAccountPasswordSet_result')
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


class unregisterVirtualAccount_args(object):
    """
    Attributes:
     - virtualMid
    """

    thrift_spec = (
        None,  # 0
        None,  # 1
        (2, TType.STRING, 'virtualMid', 'UTF8', None, ),  # 2
    )

    def __init__(self, virtualMid=None,):
        self.virtualMid = virtualMid

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
                    self.virtualMid = await iprot.readString()
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
        oprot.writeStructBegin('unregisterVirtualAccount_args')
        if self.virtualMid is not None:
            oprot.writeFieldBegin('virtualMid', TType.STRING, 2)
            oprot.writeString(self.virtualMid)
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


class unregisterVirtualAccount_result(object):
    """
    Attributes:
     - e
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRUCT, 'e', (TalkException, TalkException.thrift_spec), None, ),  # 1
    )

    def __init__(self, e=None,):
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
            if fid == 1:
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
        oprot.writeStructBegin('unregisterVirtualAccount_result')
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