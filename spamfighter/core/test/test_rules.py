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
Тесты на L{spamfighter.core.rules}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.core.rules import RulesFactory, RuleNotFoundError, DuplicateRuleError

def RuleTestFactoryFunc(domain, message, arg1, arg2=33):
    return arg1 + arg2

class RuleTestFactoryClass(object):
    def __init__(self, arg1, arg2=33):
        self.arg1 = arg1
        self.arg2 = arg2

    def analyze(self, domain, message):
        return self.arg1 - self.arg2

class RulesFactoryTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.rules.RulesFactory}.
    """

    def setUp(self):
        self.factory = RulesFactory()

    def testRegisterRule(self):
        self.factory.registerRule(RuleTestFactoryFunc)
        self.factory.registerRule(RuleTestFactoryClass)

        self.assertRaises(DuplicateRuleError, self.factory.registerRule, RuleTestFactoryFunc)
        self.assertRaises(DuplicateRuleError, self.factory.registerRule, RuleTestFactoryClass)

    def testUnRegisterRule(self):
        self.assertRaises(RuleNotFoundError, self.factory.unregisterRule, RuleTestFactoryFunc)
        self.assertRaises(RuleNotFoundError, self.factory.unregisterRule, RuleTestFactoryClass)

        self.factory.registerRule(RuleTestFactoryFunc)
        self.factory.registerRule(RuleTestFactoryClass)
        self.factory.unregisterRule(RuleTestFactoryFunc)
        self.factory.unregisterRule(RuleTestFactoryClass)

    def testInstanciateRule(self):
        self.factory.registerRule(RuleTestFactoryFunc)
        self.factory.registerRule(RuleTestFactoryClass)

        self.assertEqual(43, self.factory.instanciateRule('RuleTestFactoryFunc', arg1=10)(None, None))
        self.assertEqual(-23, self.factory.instanciateRule('RuleTestFactoryClass', arg1=10)(None, None))

        self.assertEqual(4, self.factory.instanciateRule('RuleTestFactoryFunc', arg1=2, arg2=2)(None, None))
        self.assertEqual(0, self.factory.instanciateRule('RuleTestFactoryClass', arg1=2, arg2=2)(None, None))

        self.assertRaises(RuleNotFoundError, self.factory.instanciateRule, '__NoSUCHRULE___')
