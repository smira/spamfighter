# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.commands.apiglue}.
"""

import types

from twisted.trial import unittest
from twisted.internet import defer
from zope.interface import implements

import xmlrpclib
from spamfighter.txjsonrpc import jsonrpclib

from spamfighter.core.commands.apiglue import jsonrpc_error_translator, JSONRPC_API_Glue, xmlrpc_error_translator, XMLRPC_API_Glue
from spamfighter.core.commands import errors
from spamfighter.core.commands.command import Command, ICommand
from spamfighter.core.commands.dispatcher import install

class TestPingCommand(Command):
    implements(ICommand)

    commandName = "sf.test.pinger"
    commandSignature = { 'value' : { 'type' : types.IntType, 'required' : True } }
    resultSignature = { 'result' : { 'type' : types.IntType, 'required' : True } }

    def perform(self):
        self.result.result = self.params.value + 1

    install()

class JSON_RPCTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.apiglue.JSONRPC_API_Glue}.
    """
    def testErrorTranslator(self):
        @jsonrpc_error_translator
        def good(arg1, arg2 = 1):
            return arg1

        @jsonrpc_error_translator
        def bad():
            raise errors.CommandResultMissingException, 'lala'

        @jsonrpc_error_translator
        def verybad():
            assert False

        self.assertEquals(22, good(22))
        self.assertRaises(jsonrpclib.Fault, bad)
        self.assertRaises(jsonrpclib.Fault, verybad)

        try:
            bad()
        except jsonrpclib.Fault, f:
            self.assertEquals(f.faultCode, errors.CommandResultMissingException.code)

        try:
            verybad()
        except jsonrpclib.Fault, f:
            self.assertEquals(f.faultCode, errors.UnexpectedException.code)

    def testDeferredErrorTranslator1(self):
        def good(arg1, arg2 = 1):
            return defer.succeed(arg1)
        good = jsonrpc_error_translator(good, deferred=True)

        return good(25).addCallback(lambda result: self.assertEquals(result, 25))

    def testDeferredErrorTranslator2(self):
        def bad():
            return defer.fail(errors.CommandResultMissingException('lala'))
        bad = jsonrpc_error_translator(bad, deferred=True)

        def checkError(failure):
            failure.trap(jsonrpclib.Fault)
            self.assertEquals(failure.value.faultCode, errors.CommandResultMissingException.code)

        return bad().addCallback(lambda _: self.assert_(False)).addErrback(checkError)

    def testDeferredErrorTranslator3(self):
        def verybad():
            return defer.fail(KeyError('a'))
        verybad = jsonrpc_error_translator(verybad, deferred=True)

        def checkError(failure):
            failure.trap(jsonrpclib.Fault)
            self.assertEquals(failure.value.faultCode, errors.UnexpectedException.code)

        return verybad().addCallback(lambda _: self.assert_(False)).addErrback(checkError)

    def testGetFunction(self):
        resource = JSONRPC_API_Glue()

        return resource._getFunction("sf.test.pinger")({'value' : 34}).addCallback(lambda result: self.assertEquals({'result' : 35}, result))

    def testGetFunctionNoSuchParam(self):
        try:
            JSONRPC_API_Glue()._getFunction("sf.test.pinger")({"xxx" : "yyyy"})
        except jsonrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.UnknownParameterException.code)
        else:
            self.assert_(False)

    def testGetFunctionUnknownType(self):
        try:
            JSONRPC_API_Glue()._getFunction("sf.test.pinger")({"value" : "yyyy"})
        except jsonrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.TypeParameterException.code)
        else:
            self.assert_(False)

    def testGetFunctionNoSuchFunction(self):
        try:
            JSONRPC_API_Glue()._getFunction("sf.test.absent")
        except jsonrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.CommandUnknownException.code)
        else:
            self.assert_(False)

class XML_RPCTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.apiglue.XMLRPC_API_Glue}.
    """
    def testErrorTranslator(self):
        @xmlrpc_error_translator
        def good(arg1, arg2 = 1):
            return arg1

        @xmlrpc_error_translator
        def bad():
            raise errors.CommandResultMissingException, 'lala'

        @xmlrpc_error_translator
        def verybad():
            assert False

        self.assertEquals(22, good(22))
        self.assertRaises(xmlrpclib.Fault, bad)
        self.assertRaises(xmlrpclib.Fault, verybad)

        try:
            bad()
        except xmlrpclib.Fault, f:
            self.assertEquals(f.faultCode, errors.CommandResultMissingException.code)

        try:
            verybad()
        except xmlrpclib.Fault, f:
            self.assertEquals(f.faultCode, errors.UnexpectedException.code)

    def testDeferredErrorTranslator1(self):
        def good(arg1, arg2 = 1):
            return defer.succeed(arg1)
        good = xmlrpc_error_translator(good, deferred=True)

        return good(25).addCallback(lambda result: self.assertEquals(result, 25))

    def testDeferredErrorTranslator2(self):
        def bad():
            return defer.fail(errors.CommandResultMissingException('lala'))
        bad = xmlrpc_error_translator(bad, deferred=True)

        def checkError(failure):
            failure.trap(xmlrpclib.Fault)
            self.assertEquals(failure.value.faultCode, errors.CommandResultMissingException.code)

        return bad().addCallback(lambda _: self.assert_(False)).addErrback(checkError)

    def testDeferredErrorTranslator3(self):
        def verybad():
            return defer.fail(KeyError('a'))
        verybad = xmlrpc_error_translator(verybad, deferred=True)

        def checkError(failure):
            failure.trap(xmlrpclib.Fault)
            self.assertEquals(failure.value.faultCode, errors.UnexpectedException.code)

        return verybad().addCallback(lambda _: self.assert_(False)).addErrback(checkError)

    def testGetFunction(self):
        resource = XMLRPC_API_Glue()

        return resource._getFunction("sf.test.pinger")({'value' : 34}).addCallback(lambda result: self.assertEquals({'result' : 35}, result))

    def testGetFunctionNoSuchParam(self):
        try:
            XMLRPC_API_Glue()._getFunction("sf.test.pinger")({"xxx" : "yyyy"})
        except xmlrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.UnknownParameterException.code)
        else:
            self.assert_(False)

    def testGetFunctionUnknownType(self):
        try:
            XMLRPC_API_Glue()._getFunction("sf.test.pinger")({"value" : "yyyy"})
        except xmlrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.TypeParameterException.code)
        else:
            self.assert_(False)

    def testGetFunctionNoSuchFunction(self):
        try:
            XMLRPC_API_Glue()._getFunction("sf.test.absent")
        except xmlrpclib.Fault, e:
            self.assertEquals(e.faultCode, errors.CommandUnknownException.code)
        else:
            self.assert_(False)
