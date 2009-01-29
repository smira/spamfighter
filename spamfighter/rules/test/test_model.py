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
Тесты на L{spamfighter.rules.model}.
"""

from twisted.trial import unittest
from twisted.internet import defer

from spamfighter.rules.model import modelClassify, modelTrain
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelRuleTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.model}.
    """

    def setUp(self):
        model = BayesModel()
        model.train(u"мама мыла раму", True)
        model.train(u"папа пошел гулять", False)
        getDefaultDomain().set('testModel', model)

        self.message1 = TransitMessage(serialized={ 'text' : u'мама'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={ 'text' : u'папа'}).getMessage(getDefaultDomain())

    def tearDown(self):
        getDefaultDomain().delete('testModel')
    
    def testNoModel(self):
        return defer.maybeDeferred(modelClassify(model="__noSUCHMODEL__").analyze, domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.AttributeKeyException"))

    def testNotAModel(self):
        return defer.maybeDeferred(modelClassify(model="messageDomain").analyze, domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.NotAModelError"))

    def testNoAttribute(self):
        return defer.maybeDeferred(modelClassify(model="testModel").analyze, domain=getDefaultDomain(), message=self.message1, attribute="noSuch").addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.MessageAttributeKeyException"))

    def testClassify1(self):
        return modelClassify(model="testModel").analyze(domain=getDefaultDomain(), message=self.message1).addCallback(self.assertTrue)

    def testClassify2(self):
        return modelClassify(model="testModel").analyze(domain=getDefaultDomain(), message=self.message2).addCallback(self.assertFalse)

    def testTrain(self):
        return modelTrain(model="testModel").analyze(domain=getDefaultDomain(), message=self.message2, marker="good").addCallback(self.assertTrue)

