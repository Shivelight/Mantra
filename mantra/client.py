# -*- coding: utf-8 -*-
import sys

from .lib.TAsyncio import TAsyncioBinaryProtocol, TAsyncioCompactProtocol
from .lib.TAsyncioHttpClient import TAsyncioHttpClient
from .lib.LegyHttpClient import LegyHttpClient

# HAXX
sys.modules['thrift.TAsyncio'] = sys.modules['mantra.lib.TAsyncio']

from .service import (  # noqa
    AuthService,
    CallService,
    ChannelService,
    ChatappService,
    LiffService,
    PollService,
    ShopService,
    SquareService,
    TalkService,
)
from . import patch # noqa


def auth(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = AuthService.Client(TAsyncioBinaryProtocol(transport))
    elif protocol == "compact":
        client = AuthService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def call(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = CallService.Client(TAsyncioBinaryProtocol(transport))
    elif protocol == "compact":
        client = CallService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def channel(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = ChannelService.Client(TAsyncioBinaryProtocol(transport))
    elif protocol == "compact":
        client = ChannelService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def chatapp(url, session, legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    client = ChatappService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def liff(url, session, legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    client = LiffService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def poll(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = PollService.Client(TAsyncioBinaryProtocol(transport))
    elif protocol == "compact":
        client = PollService.Client(TAsyncioCompactProtocol(transport))
    # patch.transport.poll(transport, protocol)
    client.trans = transport
    return client


def shop(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = ShopService.Client(TAsyncioBinaryProtocol(transport))
    elif protocol == "compact":
        client = ShopService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def square(url, session, legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    client = SquareService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client


def talk(url, session, protocol='binary', legy=None):
    if legy:
        transport = LegyHttpClient(url, session)
    else:
        transport = TAsyncioHttpClient(url, session)

    if protocol == "binary":
        client = TalkService.Client(TAsyncioBinaryProtocol(transport))
        patch.binary.talk(client)
    elif protocol == "compact":
        client = TalkService.Client(TAsyncioCompactProtocol(transport))
    client.trans = transport
    return client
