# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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

