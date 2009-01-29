# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008, 2009 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# This file is part of SpamFighter.
#
# SpamFighter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpamFighter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpamFighter.  If not, see <http://www.gnu.org/licenses/>.
#

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
