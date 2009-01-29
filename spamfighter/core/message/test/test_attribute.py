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

