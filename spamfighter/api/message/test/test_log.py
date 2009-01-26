# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.message.log}.
"""

from twisted.trial import unittest
from zope.interface import implements

from spamfighter.core.commands import ICommand
from spamfighter.api.message.log import MessageLogFetchCommand
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.log import MessageLog, LogEntry
from spamfighter.core.message import TransitMessage
from spamfighter.core.storage.memory import DomainMemoryStorage, MemoryStorage
from spamfighter.utils.time import startUpTestTimer, tearDownTestTimer

class MessageLogFetchCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.log.MessageLogFetchCommand}.
    """

    def setUp(self):
        startUpTestTimer(100)
        getDefaultDomain().set('testStorage', DomainMemoryStorage(storage=MemoryStorage(cleanupInterval=0)))
        self.log = MessageLog(storage='testStorage')
        getDefaultDomain().set('testLog', self.log)

        self.message1 = TransitMessage(serialized={ 'text' : u'мама'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'папа'}).getMessage(getDefaultDomain())

        self.c = MessageLogFetchCommand()
        self.c.params.getUnserialized({'partner' : None, 'log' : 'testLog'})

        return self.log.put(message=self.message1, when=90).addCallback(lambda _: self.log.put(message=self.message2, when=95, tags=['aaa']))

    def tearDown(self):
        tearDownTestTimer()
        getDefaultDomain().delete('testStorage')
        getDefaultDomain().delete('testLog')

    def testRun1(self):
        return self.c.run().addCallback(lambda _: self.assertEquals(self.c.result.entries, 
            [LogEntry(when=90, message=self.message1, id=1), LogEntry(when=95, message=self.message2, tags=['aaa'], id=2)]))

    def testRun2(self):
        self.c.params.first = 92
        return self.c.run().addCallback(lambda _: self.assertEquals(self.c.result.entries, 
            [LogEntry(when=95, message=self.message2, tags=['aaa'], id=2)]))

    def testRun3(self):
        self.c.params.last = 92
        return self.c.run().addCallback(lambda _: self.assertEquals(self.c.result.entries, 
            [LogEntry(when=90, message=self.message1, id=1)]))

    def testRun4(self):
        self.c.params.first = 80
        self.c.params.last = 100
        self.c.params.firstID = 2
        return self.c.run().addCallback(lambda _: self.assertEquals(self.c.result.entries, 
            [LogEntry(when=95, message=self.message2, tags=['aaa'], id=2)]))
