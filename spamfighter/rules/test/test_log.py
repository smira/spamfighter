# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.rules.log}.
"""

from twisted.trial import unittest
from twisted.internet import defer

from spamfighter.rules.log import messageLogPut
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.log import MessageLog, LogEntry
from spamfighter.core.storage.memory import DomainMemoryStorage, MemoryStorage
from spamfighter.utils.time import startUpTestTimer, tearDownTestTimer

class MessageLogPutTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.log.messageLogPut}.
    """

    def setUp(self):
        startUpTestTimer(100)
        getDefaultDomain().set('testStorage', DomainMemoryStorage(storage=MemoryStorage(cleanupInterval=0)))
        self.log = MessageLog(storage='testStorage')
        getDefaultDomain().set('testLog', self.log)

        self.message1 = TransitMessage(serialized={ 'text' : u'мама'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'папа'}).getMessage(getDefaultDomain())

    def tearDown(self):
        tearDownTestTimer()
        getDefaultDomain().delete('testStorage')
        getDefaultDomain().delete('testLog')

    def testNoLog(self):
        return defer.maybeDeferred(messageLogPut, log="__noSUCHLOG__", domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.AttributeKeyException"))

    def testNotALog(self):
        return defer.maybeDeferred(messageLogPut, log="messageDomain", domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.NotAMessageLogError"))

    def testPut1(self):
        return defer.maybeDeferred(messageLogPut, log="testLog", domain=getDefaultDomain(), message=self.message2).addCallback(lambda _: self.log.fetch()) \
                .addCallback(self.assertEquals, [LogEntry(when=100, tags=[], message=TransitMessage(message=self.message2), id=1)])

    def testPut2(self):
        return defer.maybeDeferred(messageLogPut, log="testLog", domain=getDefaultDomain(), message=self.message1, tag='oops').addCallback(lambda _: self.log.fetch()) \
                .addCallback(self.assertEquals, [LogEntry(when=100, tags=['oops'], message=TransitMessage(message=self.message1), id=1)])
