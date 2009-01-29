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
Тесты на L{spamfighter.utils.time}.
"""

import time as sys_time

from twisted.trial import unittest

from spamfighter.utils.time import time, startUpTestTimer, advanceTestTimer, setTestTimer, tearDownTestTimer, _inaccurate_timer_tick

class InaccurateTimeTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.time} - вариант расчета времени с точностью до 1 с.
    """
    def testTime(self):
        _inaccurate_timer_tick()
        self.assert_((int(sys_time.time())-time()) <= 1)

class TestTimerTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.time} - таймер для тестов
    """

    def setUp(self):
        startUpTestTimer(10)

    def tearDown(self):
        tearDownTestTimer()

    def testStartUp(self):
        self.assertEquals(10, time())

    def testAdvance(self):
        advanceTestTimer(20)
        self.assertEquals(30, time())

    def testSet(self):
        setTestTimer(40)
        self.assertEquals(40, time())

    def testTearDown(self):
        tearDownTestTimer()
        _inaccurate_timer_tick()
        self.assert_((int(sys_time.time())-time()) <= 1)
        startUpTestTimer(10)
