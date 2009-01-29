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
Тесты на L{spamfighter.api.domain.get}.
"""

from zope.interface import implements, Interface
from twisted.trial import unittest

from spamfighter.api.domain.get import DomainGetCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.domain import getDefaultDomain

class I1(Interface):
    pass

class I2(Interface):
    pass

class BaseTestObject(object):
    implements(I1)

class TestObject(BaseTestObject):
    implements(I2)
    def __repr__(self):
        return 'testing object representation'

class DomainGetCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.domain.get.DomainGetCommand}.
    """
    def setUp(self):
        getDefaultDomain().set('testVALUE', 33)
        getDefaultDomain().set('testOBJECT', TestObject())

    def tearDown(self):
        getDefaultDomain().delete('testVALUE')
        getDefaultDomain().delete('testOBJECT')

    def testRunNonexistent(self):
        c = DomainGetCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.name = 'NONEXISTENT'
        return c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap("spamfighter.core.commands.errors.AttributeKeyException"))
        
    def testRunSimpleValue(self):
        c = DomainGetCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.name = 'testVALUE'
        
        def checkResults(_):
            self.assertEqual(c.result.repr, '33')
            self.assertEqual(c.result.classname, 'int')
            self.assertEqual(c.result.interfaces, [])

        return c.run().addCallback(checkResults)

    def testRunObjectValue(self):
        c = DomainGetCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.name = 'testOBJECT'
        
        def checkResults(_):
            self.assertEqual(c.result.repr, 'testing object representation')
            self.assertEqual(c.result.classname, 'TestObject')
            self.assertEqual(c.result.interfaces, ['I2', 'I1'])

        return c.run().addCallback(checkResults)
