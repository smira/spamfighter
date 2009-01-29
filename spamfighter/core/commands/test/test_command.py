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
Тесты на L{spamfighter.core.commands.command}.
"""

import types

from twisted.trial import unittest
from twisted.internet import defer, reactor
from zope.interface import implements

from spamfighter.core.commands import command, errors
from spamfighter.core.commands.serialize import ISerializable, register_serializer

class IFakeSerializable(ISerializable):
    pass

class FakeSerializable(object):
    register_serializer(ISerializable)
    implements(IFakeSerializable)

    def __init__(self, value):
        self.value = value

    def serialize(self):
        d = defer.Deferred()
        reactor.callLater(0, d.callback, { 'v' : self.value })
        return d

    @classmethod
    def unserialize(cls, serialized):
        return serialized['v']

class FakeCommand(command.Command):
    implements(command.ICommand)

    commandName = 'sf.test.test'

    commandSignature = {
                        'intreq' : { 'type' : types.IntType, 'required' : True },
                        'intopt' : { 'type' : types.IntType, 'required' : False },
                       }

    resultSignature  = {
                        'ping_result' : { 'type' : types.IntType, 'required' : True },
                        'complex_result' : { 'type' : IFakeSerializable, 'required' : False },
                        'complex_result2' : { 'type' : IFakeSerializable, 'required' : False },
                        'array_result' : { 'type' : command.Array(types.IntType), 'required' : False },
                        'array_result2' : { 'type' : command.Array(IFakeSerializable), 'required' : False },
                       }

    def perform(self):
        self.result.ping_result = self.params.ping + 1
    
        return defer.succeed(self)


class CommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.command.Command}.

    Тестируем базовую функциональность команды.
    """

    def setUp(self):
        self.c = FakeCommand()

    def testParams(self):
        self.c.params.intreq = 3

        self.failUnlessEqual(self.c.params.intreq, 3)

        self.assertRaises(AttributeError, lambda x: self.c.params.no_such_param, None)

    def testCompleteness(self):
        self.assertRaises(errors.CommandParamsMissingException, self.c.checkParams)
        self.c.params.intopt = 5
        self.assertRaises(errors.CommandParamsMissingException, self.c.checkParams)
        self.c.params.intreq = 4
        self.c.checkParams()

    def testType(self):
        def wrongAssign1():
            self.c.params.intreq = 'xxx'

        def wrongAssign2():
            self.c.result.complex_result = 'xxx'

        self.assertRaises(TypeError, wrongAssign1)
        self.assertRaises(TypeError, wrongAssign2)

    def testSerialize(self):
        def gotResponse(response):
            self.failUnlessEqual(response, {'ping_result' : 4})

        self.c.result.ping_result = 4

        d = self.c.getResponse()
        d.addCallback(gotResponse)
        return d

    def testSerializeComplex(self):
        def gotResponse(response):
            self.failUnlessEqual(response, {
                'ping_result' : 10, 
                'complex_result' : {'v' : 'lala@lala'},
                'complex_result2' : {'v' : 'lala@lala2'},
                })

        self.c.result.ping_result = 10
        self.c.result.complex_result = FakeSerializable('lala@lala')
        self.c.result.complex_result2 = FakeSerializable('lala@lala2')

        d = self.c.getResponse()
        d.addCallback(gotResponse)
        return d

    def testSerializeComplexArray(self):
        def gotResponse(response):
            self.failUnlessEqual(response, {
                'ping_result' : 11, 
                'array_result2' : [{'v' : 'lala@lala'}, {'v' : 'lala@lala2'}],
                })

        self.c.result.ping_result = 11
        self.c.result.array_result2 = [FakeSerializable('lala@lala'), FakeSerializable('lala@lala2')]

        d = self.c.getResponse()
        d.addCallback(gotResponse)
        return d
