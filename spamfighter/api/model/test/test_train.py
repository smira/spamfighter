# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.model.train}.
"""

from twisted.trial import unittest

from spamfighter.api.model.train import ModelTrainCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelTrainCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.model.train.ModelTrainCommand}.
    """

    def setUp(self):
        getDefaultDomain().set('testModel', BayesModel())

    def tearDown(self):
        getDefaultDomain().delete('testModel')

    def testRun(self):
        c = ModelTrainCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={ 'text' : u'Is this SPAM?'})
        c.params.marker = 'bad'
        c.params.model = 'testModel'
        return c.run()

    def testBadMarker(self):
        c = ModelTrainCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={ 'text' : u'Is this SPAM?'})
        c.params.marker = '?'
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.TypeParameterException"))
