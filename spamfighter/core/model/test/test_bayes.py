# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.model.bayes}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IModel
from spamfighter.core.model.bayes import BayesModel
from spamfighter.core.model.test import Texts

class BayesModelTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.model.dm.BayesModel}.
    """

    def testInterface(self):
        ziv.verifyClass(IModel, BayesModel)

    def testTrainClassifySimple(self):
        model = BayesModel()
        model.train(u"мама мыла раму", True)
        model.train(u"папа пошел гулять", False)
        return model.classify(u"папа").addCallback(lambda result: self.assert_(not result)). \
                addCallback(lambda _: model.classify(u"мама")).addCallback(lambda result: self.assert_(result))

    def testTrainClassify(self):
        model = BayesModel()
        model.train(Texts.pushkin2, True)
        model.train(Texts.udaff, False)
        return model.classify(Texts.udaff2).addCallback(lambda result: self.assert_(not result)). \
                addCallback(lambda _: model.classify(Texts.pushkin)).addCallback(lambda result: self.assert_(result))

