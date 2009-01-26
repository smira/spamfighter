# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
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
Тесты на L{spamfighter.core.counters}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest
from twisted.internet import reactor

from spamfighter.core.counters import IAtomCounter, ICounter, AtomCounterPeriod, AtomCounterEternal, Counter, SpeedCounter

class AtomCounterPeriodTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.counters.AtomCounterPeriod}.
    """

    def tearDown(self):
        for call in reactor.getDelayedCalls():
            call.cancel()

    def testInterface(self):
        ziv.verifyClass(IAtomCounter, AtomCounterPeriod)

    def testLabel(self):
        self.assertEquals("за 30 секунд", AtomCounterPeriod(30).label())
        self.assertEquals("за 5 минут", AtomCounterPeriod(300).label())

    def testIncrement(self):
        c = AtomCounterPeriod(10)
        self.assertEquals(0, c.value())
        self.assertEquals(1, c.count())
        c.increment(10)
        self.assertEquals(0, c.value())
        self.assertEquals(1, c.count())
        c.exchangeCounters()
        self.assertEquals(10, c.value())
        self.assertEquals(1, c.count())
        c.increment(20)
        c.increment(15)
        c.exchangeCounters()
        self.assertEquals(35, c.value())
        self.assertEquals(2, c.count())

    def testPeriod(self):
        self.assertEquals(33, AtomCounterPeriod(33).period())
       
class AtomCounterEternalTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.counters.AtomCounterEternal}.
    """

    def testInterface(self):
        ziv.verifyClass(IAtomCounter, AtomCounterEternal)

    def testLabel(self):
        self.assertEquals("за всё время", AtomCounterEternal().label())

    def testIncrement(self):
        c = AtomCounterEternal()
        self.assertEquals(0, c.value())
        self.assertEquals(1, c.count())
        c.increment(10)
        c.increment(15)
        self.assertEquals(25, c.value())
        self.assertEquals(2, c.count())

    def testPeriod(self):
        self.assertEquals(1, AtomCounterEternal().period())

class TestCounter(Counter):
    def __init__(self):
        self.counters = [AtomCounterEternal(), AtomCounterPeriod(30*60)]

    def format(self):
        return "%s: %d"

class CounterTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.counters.Counter}.
    """

    def tearDown(self):
        for call in reactor.getDelayedCalls():
            call.cancel()

    def testInterface(self):
        ziv.verifyClass(ICounter, Counter)

    def testStr(self):
        c = TestCounter()
        c.increment(10)
        self.assertEquals("за всё время: 10, за 30 минут: 0", str(c))

    def testPickling(self):
        import pickle

        c = TestCounter()
        c.increment(10)
        s = pickle.dumps(c)
        c2 = pickle.loads(s)
        self.assertEquals("за всё время: 0, за 30 минут: 0", str(c2))

