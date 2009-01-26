# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.commands.serialize}.
"""

import datetime
import copy

from twisted.trial import unittest

from spamfighter.core.commands.serialize import DateTime, register_serializer, get_serializer, serializers, ISerializable, SerializerNotFoundException

class INotSerializableInterface(object):
    pass

class ISerializableInterface(ISerializable):
    pass

class SerializabeClass(object):
    register_serializer(ISerializableInterface)
    pass

class RegisterTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.core.commands.serialize.register_serializer}, L{spamfighter.core.commands.serialize.get_serializer}.
    """

    def test_get_serializer(self):
        self.assertEquals(SerializabeClass, get_serializer(ISerializableInterface))

    def test_get_absent_serializer(self):
        self.assertRaises(SerializerNotFoundException, get_serializer, INotSerializableInterface)

class DateTimeTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.core.commands.serialize.DateTime}.
    """

    def test_init_str(self):
        self.assertEquals("20080618T10:37:33", str(DateTime("20080618T10:37:33")))

    test_init_str.skip = 'Конструктор у DateTime ни фига не переопределяется'

    def test_toISO(self):
        self.assertEquals("20080618T10:37:33", DateTime.toISO(datetime.datetime(2008, 06, 18, 10, 37, 33)))
        self.assertEquals(None, DateTime.toISO(None))

    def test_fromISO(self):
        self.assertEquals(datetime.datetime(2008, 06, 18, 10, 37, 33), DateTime.fromISO("20080618T10:37:33"))

