# -*- test-case-name: twisted.web.test.test_jsonrpc -*-
#
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.

"""Test JSON-RPC support."""

import time

from twisted.trial import unittest
from twisted.web import server, static
from twisted.internet import reactor, defer
from twisted.python import log

from spamfighter.txjsonrpc import jsonrpclib
from spamfighter.txjsonrpc.web import jsonrpc
from spamfighter.txjsonrpc.web.jsonrpc import JSONRPC, addIntrospection

class TestRuntimeError(RuntimeError):
    pass

class TestValueError(ValueError):
    pass

class Test(JSONRPC):

    FAILURE = 666
    NOT_FOUND = 23
    SESSION_EXPIRED = 42

    # the doc string is part of the test
    def jsonrpc_add(self, a, b):
        """This function add two numbers."""
        return a + b

    jsonrpc_add.signature = [['int', 'int', 'int'],
                            ['double', 'double', 'double']]

    # the doc string is part of the test
    def jsonrpc_pair(self, string, num):
        """This function puts the two arguments in an array."""
        return [string, num]

    jsonrpc_pair.signature = [['array', 'string', 'int']]

    # the doc string is part of the test
    def jsonrpc_defer(self, x):
        """Help for defer."""
        return defer.succeed(x)

    def jsonrpc_deferFail(self):
        return defer.fail(TestValueError())

    # don't add a doc string, it's part of the test
    def jsonrpc_fail(self):
        raise TestRuntimeError

    def jsonrpc_fault(self):
        return jsonrpclib.Fault(12, "hello")

    def jsonrpc_deferFault(self):
        return defer.fail(jsonrpclib.Fault(17, "hi"))

    def jsonrpc_complex(self):
        return {"a": ["b", "c", 12, []], "D": "foo"}

    def jsonrpc_dict(self, map, key):
        return map[key]

    def _getFunction(self, functionPath):
        try:
            return JSONRPC._getFunction(self, functionPath)
        except jsonrpclib.NoSuchFunction:
            if functionPath.startswith("SESSION"):
                raise jsonrpclib.Fault(self.SESSION_EXPIRED, "Session non-existant/expired.")
            else:
                raise

    jsonrpc_dict.help = 'Help for dict.'

class TestAuthHeader(Test):
    """
    This is used to get the header info so that we can test
    authentication.
    """
    def __init__(self):
        Test.__init__(self)
        self.request = None

    def render(self, request):
        self.request = request
        return Test.render(self, request)

    def jsonrpc_authinfo(self):
        return self.request.getUser(), self.request.getPassword()

class JSONRPCTestCase(unittest.TestCase):

    def setUp(self):
        self.p = reactor.listenTCP(0, server.Site(Test()),
                                   interface="127.0.0.1")
        self.port = self.p.getHost().port

    def tearDown(self):
        return self.p.stopListening()

    def proxy(self):
        return jsonrpc.Proxy("http://127.0.0.1:%d/" % self.port)

    def testResults(self):
        inputOutput = [
            ("add", (2, 3), 5),
            ("defer", ("a",), "a"),
            ("dict", ({"a": 1}, "a"), 1),
            ("pair", ("a", 1), ["a", 1]),
            ("complex", (), {"a": ["b", "c", 12, []], "D": "foo"})]

        dl = []
        for meth, args, outp in inputOutput:
            d = self.proxy().callRemote(meth, *args)
            d.addCallback(self.assertEquals, outp)
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)

    def testErrors(self):
        dl = []
        for code, methodName in [(666, "fail"), (666, "deferFail"),
                                 (12, "fault"), (-32601, "noSuchMethod"),
                                 (17, "deferFault"), (42, "SESSION_TEST")]:
            d = self.proxy().callRemote(methodName)
            d = self.assertFailure(d, jsonrpclib.Fault)
            d.addCallback(lambda exc, code=code: self.assertEquals(exc.faultCode, code))
            dl.append(d)
        d = defer.DeferredList(dl, fireOnOneErrback=True)
        d.addCallback(lambda ign: self.flushLoggedErrors())
        return d


class JSONRPCTestCase2(JSONRPCTestCase):
    """Test with proxy that doesn't add a slash."""

    def proxy(self):
        return jsonrpc.Proxy("http://127.0.0.1:%d" % self.port)


class JSONRPCTestAuthenticated(JSONRPCTestCase):
    """
    Test with authenticated proxy. We run this with the same inout/ouput as
    above.
    """
    user = "username"
    password = "asecret"

    def setUp(self):
        self.p = reactor.listenTCP(0, server.Site(TestAuthHeader()),
                                   interface="127.0.0.1")
        self.port = self.p.getHost().port


    def testAuthInfoInURL(self):
        p = jsonrpc.Proxy("http://%s:%s@127.0.0.1:%d/" % (self.user, self.password, self.port))
        return p.callRemote("authinfo").addCallback(self.assertEquals, [self.user, self.password])


    def testExplicitAuthInfo(self):
        p = jsonrpc.Proxy("http://127.0.0.1:%d/" % (self.port,), self.user, self.password)
        return p.callRemote("authinfo").addCallback(self.assertEquals, [self.user, self.password])


    def testExplicitAuthInfoOverride(self):
        p = jsonrpc.Proxy("http://wrong:info@127.0.0.1:%d/" % (self.port,), self.user, self.password)
        return p.callRemote("authinfo").addCallback(self.assertEquals, [self.user, self.password])



class JSONRPCTestIntrospection(JSONRPCTestCase):

    def setUp(self):
        jsonrpc = Test()
        addIntrospection(jsonrpc)
        self.p = reactor.listenTCP(0, server.Site(jsonrpc),interface="127.0.0.1")
        self.port = self.p.getHost().port

    def testListMethods(self):

        def cbMethods(meths):
            meths.sort()
            self.failUnlessEqual(
                meths,
                ['add', 'complex', 'defer', 'deferFail',
                 'deferFault', 'dict', 'fail', 'fault',
                 'pair', 'system.listMethods',
                 'system.methodHelp',
                 'system.methodSignature'])

        d = self.proxy().callRemote("system.listMethods")
        d.addCallback(cbMethods)
        return d

    def testMethodHelp(self):
        inputOutputs = [
            ("defer", "Help for defer."),
            ("fail", ""),
            ("dict", "Help for dict.")]

        dl = []
        for meth, expected in inputOutputs:
            d = self.proxy().callRemote("system.methodHelp", meth)
            d.addCallback(self.assertEquals, expected)
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)

    def testMethodSignature(self):
        inputOutputs = [
            ("defer", ""),
            ("add", [['int', 'int', 'int'],
                     ['double', 'double', 'double']]),
            ("pair", [['array', 'string', 'int']])]

        dl = []
        for meth, expected in inputOutputs:
            d = self.proxy().callRemote("system.methodSignature", meth)
            d.addCallback(self.assertEquals, expected)
            dl.append(d)
        return defer.DeferredList(dl, fireOnOneErrback=True)


class JSONRPCClientErrorHandling(unittest.TestCase):
    def setUp(self):
        self.resource = static.File(__file__)
        self.resource.isLeaf = True
        self.port = reactor.listenTCP(0, server.Site(self.resource), interface='127.0.0.1')

    def tearDown(self):
        return self.port.stopListening()

    def testErroneousResponse(self):
        proxy = jsonrpc.Proxy("http://127.0.0.1:%d/" % (self.port.getHost().port,))
        return self.assertFailure(proxy.callRemote("someMethod"), Exception)
