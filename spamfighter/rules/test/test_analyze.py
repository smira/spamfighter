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
Тесты на L{spamfighter.rules.analyze}.
"""

from twisted.trial import unittest

from spamfighter.rules.analyze import messageFloodCheck
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain

class AnalyzeRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.text}.
    """

    def setUp(self):
        self.message5 = TransitMessage(serialized={ 'text' : u'!!!!!!!!!!!!!!!!!!!!!!', 'from': 16}).getMessage(getDefaultDomain())
        self.message6 = TransitMessage(serialized={ 'text' : u'покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи!', 'from': 16}).getMessage(getDefaultDomain())

    def tearDown(self):
        pass

    def testAnalyzeMessage(self):
        self.assertFalse(messageFloodCheck(domain=getDefaultDomain(), message=self.message5))
        self.assertTrue(messageFloodCheck(domain=getDefaultDomain(), message=self.message5, minLength=30))
        self.assertFalse(messageFloodCheck(domain=getDefaultDomain(), message=self.message6))
