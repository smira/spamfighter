# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.utils.registrator}.
"""

import unittest
from spamfighter.utils.registrator import registrator

@registrator
def testRegistrator(cls):
    global testCls
    testCls = cls

class TestClass(object):
    testRegistrator()

class RegistratorTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.registrator.registrator}.
    """
    def test_Registrator(self):
        global testCls
        self.assertEquals(testCls, TestClass)
