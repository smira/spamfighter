# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.message.attribute}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IAttribute, IAttributeDomain
from spamfighter.core.message.attribute import Attribute, AttributeDomain, TextAttributeDomain, IntAttributeDomain

class AttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.AttributeDomain}.
    """
    def testInterface(self):
        ziv.verifyClass(IAttributeDomain, AttributeDomain)

    def testName(self):
        self.assertEquals('John', AttributeDomain('John').name())

class TextAttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.TextAttributeDomain}.
    """
    def testSerialize(self):
        ta = TextAttributeDomain('John')
        a = Attribute('John', u'Ураа!')
        self.assertEquals('Ураа!', ta.serialize(a))
        a = Attribute('John', 'Ураа!')
        self.assertEquals('Ураа!', ta.serialize(a))

    def testDeserialize(self):
        ta = TextAttributeDomain('John')
        self.assertEquals(u'Ураа!', ta.deserialize('Ураа!').value())
        self.assert_(ta is ta.deserialize('Ураа!').domain())
        self.assertEquals(u'Ураа!', ta.deserialize(u'Ураа!').value())

    def testDeserializeStrip(self):
        ta = TextAttributeDomain('John')
        self.assertEquals(u'Ураа!', ta.deserialize(' Ураа! ').value())

class IntAttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.IntAttributeDomain}.
    """
    def testSerialize(self):
        ta = IntAttributeDomain('John')
        a = Attribute('John', 1586)
        self.assertEquals(1586, ta.serialize(a))

    def estDeserialize(self):
        ta = IntAttributeDomain('John')
        self.assertEquals(1586, ta.deserialize(1586).value())
        self.assert_(ta is ta.deserialize(1586).domain())

class AttributeTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.Attribute}.
    """
    def setUp(self):
        self.attribute = Attribute(TextAttributeDomain('John'), 'abcd')

    def testInterface(self):
        ziv.verifyClass(IAttribute, Attribute)

    def testDomain(self):
        self.assertEquals(AttributeDomain('John'), self.attribute.domain())

    def testSerialize(self):
        self.assertEquals('abcd', self.attribute.serialize())

