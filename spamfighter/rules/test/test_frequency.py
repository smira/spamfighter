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
Тесты на L{spamfighter.rules.frequency}.
"""

from twisted.internet import defer
from twisted.trial import unittest

from spamfighter.utils.time import startUpTestTimer, advanceTestTimer, tearDownTestTimer
from spamfighter.rules.frequency import messageFrequencyCheck, calculateMD5, clearMessage, userFrequencyCheck
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.storage.memory import DomainMemoryStorage, MemoryStorage

class FrequencyRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.frequency}.
    """

    def setUp(self):
        getDefaultDomain().set('testStorage', DomainMemoryStorage(storage=MemoryStorage(cleanupInterval=0)))

        self.message1 = TransitMessage(serialized={ 'text' : u'мама мыла раму папы', 'ip': '192.168.140.4'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'папа'}).getMessage(getDefaultDomain())
        self.message3 = TransitMessage(serialized={ 'text' : u'привет всем в чате!', 'from': 15}).getMessage(getDefaultDomain())
        self.message4 = TransitMessage(serialized={ 'text' : u'и тебе привет!', 'from': 16, 'ip': '192.168.140.4'}).getMessage(getDefaultDomain())
        startUpTestTimer(1000)

    def tearDown(self):
        getDefaultDomain().delete('testStorage')
        tearDownTestTimer()

    def testCalculateMD5(self):
        self.assertEquals('f6b9cb6316325114b93fc8d32399bece', calculateMD5(u'мама не помыла раму'))

    def testClearMessage(self):
        self.assertEquals(u'мамамыламыламыла', clearMessage(u'Мама мыла, мыла, мыла!!!!'))

    def testFrequencyCheckOneMessage(self):
        return messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage="testStorage", timeout=10, count=2). \
                addCallback(self.assertTrue)

    def testCountMessages(self):
        d = defer.succeed(None)

        for i in xrange(15):
            d.addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage="testStorage", count=16, timeout=10). \
                addCallback(self.assertTrue))

        d.addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)). \
        addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertTrue))

        return d

    def testFrequencyCheckOneUser(self):
        return messageFrequencyCheck(domain=getDefaultDomain(), message=self.message3, storage="testStorage", timeout=10, count=2). \
                addCallback(self.assertTrue)

    def testCountUserMessages(self):
        d = defer.succeed(None)

        for i in xrange(15):
            d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage="testStorage", count=16, timeout=10). \
                addCallback(self.assertTrue))

        d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)). \
        addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertTrue))

        return d

    def testCountIPMessages(self):
        d = defer.succeed(None)

        for i in xrange(15):
            d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute="ip", storage="testStorage", count=16, timeout=10). \
                addCallback(self.assertTrue))

        d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute="ip", storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)). \
        addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute="ip", storage="testStorage", count=16, timeout=10). \
            addCallback(self.assertTrue))

        return d
