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

