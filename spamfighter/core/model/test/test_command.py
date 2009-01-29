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
Тесты на L{spamfighter.core.model.command}.
"""

from twisted.trial import unittest
from zope.interface import implements

from spamfighter.core.commands import ICommand
from spamfighter.core.model.command import ModelBaseCommand
from spamfighter.core.model.bayes import BayesModel
from spamfighter.core.domain import getDefaultDomain

class FakeModelCommand(ModelBaseCommand):
    implements(ICommand)

    commandName = 'sf.test.model'

    commandSignature = {
                       }

    resultSignature  = {
                       }

    def perform(self):
        return None

class ModelBaseCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.model.command.ModelBaseCommand}.
    """

    def setUp(self):
        self.c = FakeModelCommand()
        self.model = BayesModel()
        getDefaultDomain().set('testMODEL', self.model)

    def tearDown(self):
        getDefaultDomain().delete('testMODEL')

    def testNoSuchModel(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'noSuchModel', 'message' : {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AttributeKeyException'))

    def testNotAModel(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'messageDomain', 'message' : {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.NotAModelError'))

    def testGetModel(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'testMODEL', 'message' : {'text' : u''}})
        return self.c.run().addCallback(lambda _: self.assert_(self.c.model is self.model))

    def testGetNoText(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'testMODEL', 'message' : {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.MessageAttributeKeyException'))

    def testGetText1(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'testMODEL', 'message' : {'text' : u'Hoora!'}})
        return self.c.run().addCallback(lambda _: self.assertEqual('Hoora!', self.c.text))

    def testGetText2(self):
        self.c.params.getUnserialized({'partner' : None, 'model' : 'testMODEL', 'message' : {'text' : u'Hoora!'}, 'text_attribute' : 'text1'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.MessageAttributeKeyException'))

