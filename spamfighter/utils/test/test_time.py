# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
