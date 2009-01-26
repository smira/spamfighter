# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
