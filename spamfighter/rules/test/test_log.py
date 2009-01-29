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
