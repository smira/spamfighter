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
Тесты на L{spamfighter.core.storage.memory}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IExpirableStorage, IUnreliableStorage, IDomainBindable
from spamfighter.utils.time import advanceTestTimer
from spamfighter.core.storage.memory import MemoryStorage, DomainMemoryStorage
from spamfighter.core.storage.test.base import ExpirableStorageTestMixin
from spamfighter.core.domain import getDefaultDomain

class MemoryStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.memory.MemoryStorage}.
    """

    def setUp(self):
        ExpirableStorageTestMixin.setUp(self)
        self.s = MemoryStorage(cleanupInterval=0)

    def tearDown(self):
        ExpirableStorageTestMixin.tearDown(self)

    def testInterface(self):
        ziv.verifyClass(IExpirableStorage, MemoryStorage)
        ziv.verifyClass(IUnreliableStorage, MemoryStorage)

    def testCleanup(self):
        def checkState1(_):
            self.assertEquals(self.s.deleteQueue, { 100 : { 'key1' : 1 }, 101 : { 'key2' : 1 }})
            self.assertEquals(self.s.hash, { 'key1' : (1005, 'value1'), 'key2' : (1015, 'value2') })
            self.assertEquals(self.s.lastDeleteTime, 100)

        def checkState2(_):
            self.assertEquals(self.s.deleteQueue, { 101 : { 'key2' : 1 }})
            self.assertEquals(self.s.hash, { 'key2' : (1015, 'value2') })
            self.assertEquals(self.s.lastDeleteTime, 101)

        return self.s.set('key1', 'value1', 5).addCallback(lambda _: self.s.set('key2', 'value2', 15)).addCallback(checkState1) \
                .addCallback(lambda _: advanceTestTimer(12)).addCallback(lambda _: self.s._cleanup()).addCallback(checkState2)

    def testInit(self):
        self.assertEquals(self.s.lastDeleteTime, 100)

    def testSetState(self):
        def checkState1(_):
            self.assertEquals(self.s.deleteQueue, { 100 : { 'key' : 1 }})
            self.assertEquals(self.s.hash, { 'key' : (1001, 'value') })

        def checkState2(_):
            self.assertEquals(self.s.deleteQueue, { 100 : {}, 102 : { 'key' : 1 }})
            self.assertEquals(self.s.hash, { 'key' : (1020, 'value2') })

        return self.s.set('key', 'value', 1).addCallback(checkState1).addCallback(lambda _: self.s.set('key', 'value2', 20)).addCallback(checkState2)

    def testInstance(self):
        self.assert_(MemoryStorage.getInstance() is MemoryStorage.getInstance())

    def testGetExpired(self):
        def checkState(_):
            self.assertEquals(self.s.deleteQueue, { 100 : {}})
            self.assertEquals(self.s.hash, {})

        return ExpirableStorageTestMixin.testGetExpired(self).addCallback(checkState)

class DomainMemoryStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.memory.DomainMemoryStorage}.
    """

    def setUp(self):
        ExpirableStorageTestMixin.setUp(self)
        self.s = DomainMemoryStorage()
        self.s.bind(getDefaultDomain(), 'testMemory')

    def testInterface(self):
        ziv.verifyClass(IExpirableStorage, DomainMemoryStorage)
        ziv.verifyClass(IUnreliableStorage, DomainMemoryStorage)
        ziv.verifyClass(IDomainBindable, DomainMemoryStorage)

    def testPickling(self):
        import pickle

        s2 = pickle.loads(pickle.dumps(self.s))
