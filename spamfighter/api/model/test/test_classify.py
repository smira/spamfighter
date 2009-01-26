# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.model.classify}.
"""

from twisted.trial import unittest

from spamfighter.api.model.classify import ModelClassifyCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelClassifyCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.model.classify.ModelClassifyCommand}.
    """

    def setUp(self):
        model = BayesModel()
        model.train(u"мама мыла раму", True)
        model.train(u"папа пошел гулять", False)
        getDefaultDomain().set('testModel', model)

    def tearDown(self):
        getDefaultDomain().delete('testModel')

    def testRun1(self):
        c = ModelClassifyCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={ 'text' : u'мама'})
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(c.result.marker == 'good'))

    def testRun2(self):
        c = ModelClassifyCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={ 'text' : u'папа'})
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(c.result.marker == 'bad'))
