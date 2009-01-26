# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.message.message}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IMessageDomain, IMessage, ITaggedMessage
from spamfighter.core.message.message import MessageDomain, Message, TaggedMessage
from spamfighter.core.message.attribute import Attribute, AttributeDomain, AttributeNotFoundError 

class MessageDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.message.MessageDomain}.
    """
    def setUp(self):
        self.domain = MessageDomain(AttributeDomain(name='aa'), AttributeDomain(name='bb'), AttributeDomain(name='cc'))

    def testInterface(self):
        ziv.verifyClass(IMessageDomain, MessageDomain)

    def testNames(self):
        names = self.domain.names()
        names.sort()
        self.assertEquals(['aa', 'bb', 'cc'], names)

    def testGetItem(self):
        self.assertEquals(AttributeDomain(name='aa'), self.domain['aa'])
        self.assertRaises(KeyError, self.domain.__getitem__, 'xx')

class MessageTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.message.Message}.
    """
    def setUp(self):
        self.attribute = Attribute(AttributeDomain('John'), 'abcd')
        self.message = Message([self.attribute])

    def testInterface(self):
        ziv.verifyClass(IMessage, Message)

    def testGet(self):
        self.assertEquals(self.attribute, self.message.get('John'))
        self.assertRaises(AttributeNotFoundError, self.message.get, 'Mary')

class TaggedMessageTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.message.TaggedMessage}.
    """
    def setUp(self):
        self.message = TaggedMessage([])
        self.message.addTag('lala')
        self.message.addTag('tutu')

    def testInterface(self):
        ziv.verifyClass(ITaggedMessage, TaggedMessage)

    def testCheckHasAllTags(self):
        self.assertTrue(self.message.checkHasAllTags(['lala', 'tutu']))
        self.assertFalse(self.message.checkHasAllTags(['lala', 'tutu', 'abcd']))
        self.assertTrue(self.message.checkHasAllTags([]))

    def testCheckHasNoTags(self):
        self.assertTrue(self.message.checkHasNoTags(['fafa']))
        self.assertFalse(self.message.checkHasNoTags(['fafa', 'lala']))
        self.assertTrue(self.message.checkHasNoTags([]))

    def testConstructFromMessage(self):
        attribute = Attribute(AttributeDomain('John'), 'abcd')
        msg = Message([attribute])
        tagged = TaggedMessage(message=msg)
        self.assertEquals(attribute, tagged.get('John'))

    def testGetTags(self):
        self.assertEquals(['lala', 'tutu'], sorted(self.message.getTags()))

