# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
