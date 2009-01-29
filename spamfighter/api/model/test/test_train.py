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
