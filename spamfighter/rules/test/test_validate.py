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
Тесты на L{spamfighter.rules.validate}.
"""

from twisted.trial import unittest

from spamfighter.rules.validate import regexpCheck, lengthCheck, attributeCheck, hasAttribute
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain

class ValidateRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.validate}.
    """
    def setUp(self):
        self.message1 = TransitMessage(serialized={ 'text' : u'тестовое сообщение для анализа регуляркой'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'плохое тестовое сообщение для анализа регулиркой'}).getMessage(getDefaultDomain())
        self.message3 = TransitMessage(serialized={ 'text' : u'среднее тестовое сообщение', 'from' : 1212}).getMessage(getDefaultDomain())

    def tearDown(self):
        pass

    def testCheckRegexp1(self):
        self.assertTrue(regexpCheck(regexp=u'^тестовое ').analyze(domain=getDefaultDomain(), message=self.message1))

    def testCheckRegexp2(self):
        self.assertFalse(regexpCheck(regexp=u'^тестовое').analyze(domain=getDefaultDomain(), message=self.message2))

    def testCheckLength(self):
        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=64))
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=10))

    def testCheckLength(self):
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1))

        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=64))
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=10))

        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, maxLength=64))
        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, maxLength=10))

    def testCheckAttribute(self):
        self.assertTrue(attributeCheck(domain=getDefaultDomain(), message=self.message3, attribute='from', value=1212))
        self.assertFalse(attributeCheck(domain=getDefaultDomain(), message=self.message3, attribute='from', value=1412))

    def testHasAttribute(self):
        self.assertFalse(hasAttribute(domain=getDefaultDomain(), message=self.message1, attribute='from'))
        self.assertTrue(hasAttribute(domain=getDefaultDomain(), message=self.message3, attribute='from'))
