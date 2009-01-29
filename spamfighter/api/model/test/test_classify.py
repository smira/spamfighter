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
