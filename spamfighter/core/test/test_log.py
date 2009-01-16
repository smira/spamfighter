# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.log}.
"""

from twisted.internet import defer
from twisted.trial import unittest
from zope.interface import verify as ziv

from spamfighter.utils.time import startUpTestTimer, advanceTestTimer, tearDownTestTimer, time
from spamfighter.core.message import TransitMessage, TaggedMessage
from spamfighter.core.message.serialize import ISerializable
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.storage.memory import DomainMemoryStorage, MemoryStorage
from spamfighter.core.log import MessageLog, LogEntry
from spamfighter.interfaces import IMessageLog, ILogEntry

class LogEntryTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.log.LogEntry}.
    """

    def setUp(self):
        self.message1 = TransitMessage(serialized={ 'text' : u'мама мыла раму папы'}).getMessage(getDefaultDomain())
        self.message2 = TaggedMessage(TransitMessage(serialized={ 'text' : u'и тебе привет!',}).getMessage(getDefaultDomain()))
        self.message2.addTag('good')
        self.message2.addTag('bad')

    def testInterface(self):
        ziv.verifyClass(ISerializable, LogEntry)
        ziv.verifyClass(ILogEntry, LogEntry)

    def testSerialize(self):
        return LogEntry(when=101, message=self.message2, id=33).serialize().addCallback(self.assertEquals, 
                { 'when' : 101, 'tags' : ['bad', 'good'], 'message' : { 'text' : 'и тебе привет!' }, 'id' : 33})

    def testUnserialize(self):
        self.assertEquals(LogEntry(when=101, message=self.message2, id=33), LogEntry.unserialize(
                { 'when' : 101, 'tags' : ['bad', 'good'], 'message' : { 'text' : 'и тебе привет!' }, 'id' : 33}))

    def testConstructor(self):
        l = LogEntry(when=None, message=self.message1)
        self.assertEquals([], l.tags)
        self.assertEquals(time(), l.when)

        l = LogEntry(when=200, message=self.message2)
        self.assertEquals(['bad', 'good'], l.tags)
        self.assertEquals(200, l.when)

class MessageLogTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.log.MessageLog}.
    """

    def setUp(self):
        getDefaultDomain().set('testStorage', DomainMemoryStorage(storage=MemoryStorage(cleanupInterval=0)))

        self.message1 = TransitMessage(serialized={ 'text' : u'мама мыла раму папы'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'папа'}).getMessage(getDefaultDomain())
        self.message3 = TransitMessage(serialized={ 'text' : u'привет всем в чате!'}).getMessage(getDefaultDomain())
        self.message4 = TaggedMessage(TransitMessage(serialized={ 'text' : u'и тебе привет!',}).getMessage(getDefaultDomain()))
        self.message4.addTag('good')
        self.message4.addTag('bad')

        startUpTestTimer(1000)

        self.log = MessageLog(storage='testStorage')
        getDefaultDomain().set('testLog', self.log)

    def tearDown(self):
        tearDownTestTimer()
        getDefaultDomain().delete('testLog')
        getDefaultDomain().delete('testStorage')

    def testInterface(self):
        ziv.verifyClass(IMessageLog, MessageLog)

    def testPutFetch(self):
        return self.log.put(self.message1).addCallback(lambda _: self.log.fetch()) \
                .addCallback(self.assertEquals, [LogEntry(when=1000, message=self.message1, id=1)] )

    def testPutFetchLong(self):
        return self.log.put(self.message1).addCallback(lambda _: advanceTestTimer(989)).addCallback(lambda _: self.log.fetch()) \
                .addCallback(self.assertEquals, [LogEntry(when=1000, message=self.message1, id=1)] ) \
                .addCallback(lambda _: advanceTestTimer(1)).addCallback(lambda _: self.log.fetch()).addCallback(self.assertEquals, [])

    def testFirst(self):
        return defer.DeferredList([self.log.put(self.message2, when=when) for when in [850, 852, 900, 901, 920]]) \
                .addCallback(lambda _: self.log.fetch(first=852)) \
                .addCallback(lambda result: self.assertEquals([852, 900, 901, 920], map(lambda i: i.when, result)))

    def testLast(self):
        return defer.DeferredList([self.log.put(self.message2, when=when) for when in [850, 852, 900, 901, 920]]) \
                .addCallback(lambda _: self.log.fetch(last=900)) \
                .addCallback(lambda result: self.assertEquals([850, 852, 900], map(lambda i: i.when, result)))

    def testFirstLast(self):
        return defer.DeferredList([self.log.put(self.message2, when=when) for when in [850, 852, 900, 901, 920]]) \
                .addCallback(lambda _: self.log.fetch(first=852, last=901)) \
                .addCallback(lambda result: self.assertEquals([852, 900, 901], map(lambda i: i.when, result)))

    def testFirstWithShift(self):
        return defer.DeferredList([self.log.put(self.message2, when=when) for when in [850, 852, 900, 901, 920]]) \
                .addCallback(lambda _: advanceTestTimer(500)).addCallback(lambda _: self.log.fetch(first=852)) \
                .addCallback(lambda result: self.assertEquals([852, 900, 901, 920], map(lambda i: i.when, result)))

    def testFirstID(self):
        return defer.DeferredList([self.log.put(self.message2, when=when) for when in [850, 852, 900, 901, 920]]) \
                .addCallback(lambda _: self.log.fetch(first=800, firstID=3)) \
                .addCallback(lambda result: self.assertEquals([900, 901, 920], map(lambda i: i.when, result)))

    def testPickling(self):
        import pickle

        l = pickle.loads(pickle.dumps(self.log))
