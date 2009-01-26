# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
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
Тесты на L{spamfighter.core.firewall}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest
from twisted.internet import defer

from spamfighter.interfaces import IMessageAnalyzer, IMessageFirewall
from spamfighter.core.message import Message, TaggedMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.firewall import MessageFirewall, SyntaxError, FirewallStatement, FirewallMessagePack,  \
    SkipToProcess, SkipFirewallStatement, DoFirewallStatement, StopFirewallStatement, FirewallResult
from spamfighter.core.commands import errors

class FirewallStatementTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.firewall.FirewallStatement}.
    """

    def setUp(self):
        self.message = TaggedMessage([])
        self.pack = FirewallMessagePack(self.message, getDefaultDomain())

    def testIfHelper(self):
        self.assertTrue(FirewallStatement()._if_helper(self.message))
        self.assertFalse(FirewallStatement(if_tags=['aaa'], if_inverted=False)._if_helper(self.message))
        self.assertTrue(FirewallStatement(if_tags=['aaa'], if_inverted=True)._if_helper(self.message))
        self.message.addTag('aaa')
        self.assertTrue(FirewallStatement(if_tags=['aaa'], if_inverted=False)._if_helper(self.message))
        self.assertFalse(FirewallStatement(if_tags=['aaa'], if_inverted=True)._if_helper(self.message))

    def testCompile1(self):
        d = FirewallStatement(label=101).compile(defer.fail(SkipToProcess(101, self.pack)))
        def checkPack(pack):
            self.assert_(pack is self.pack)
        d.addCallback(checkPack)
        return d

    def testCompile2(self):
        d = FirewallStatement(label=131).compile(defer.fail(SkipToProcess(101, self.pack)))
        d.addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(SkipToProcess))
        return d

    def testCompile3(self):
        d = FirewallStatement(label=101).compile(defer.fail(SkipToProcess(101, self.pack)))
        d.addCallback(lambda pack: self.assert_(pack is self.pack))
        return d

    def testStr(self):
        self.assertEquals("if not aaa, bbb ", str(FirewallStatement(if_tags=['aaa', 'bbb'], if_inverted=True)))
        self.assertEquals("if aaa, bbb ", str(FirewallStatement(if_tags=['aaa', 'bbb'], if_inverted=False)))
        self.assertEquals("377: if aaa, bbb ", str(FirewallStatement(label=377, if_tags=['aaa', 'bbb'], if_inverted=False)))
        self.assertEquals("377: ", str(FirewallStatement(label=377)))

class SkipFirewallStatementTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.firewall.SkipFirewallStatement}.
    """

    def setUp(self):
        self.message = TaggedMessage([])
        self.pack = FirewallMessagePack(self.message, getDefaultDomain())

    def testCompile1(self):
        d = SkipFirewallStatement(skip_label=201).compile(defer.succeed(self.pack))
        def checkSkipTo(failure):
            failure.trap(SkipToProcess)
            self.assert_(failure.value.label == 201)
            self.assert_(failure.value.pack is self.pack)
        d.addCallback(lambda _: self.assert_(False)).addErrback(checkSkipTo)
        return d

    def testCompile2(self):
        def checkPack(pack):
            self.assert_(pack is self.pack)

        d = SkipFirewallStatement(skip_label=201, if_tags=['aaa'], if_inverted=False).compile(defer.succeed(self.pack)).addCallback(checkPack)
        return d

    def testStr(self):
        self.assertEquals('skip to 201', str(SkipFirewallStatement(skip_label=201)))
        self.assertEquals('100: skip to 201', str(SkipFirewallStatement(skip_label=201, label=100)))

class StopFirewallStatementTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.firewall.StopFirewallStatement}.
    """

    def setUp(self):
        self.message = TaggedMessage([])
        self.pack = FirewallMessagePack(self.message, getDefaultDomain())

    def testCompile1(self):
        d = StopFirewallStatement(stop_marker='SPAM').compile(defer.succeed(self.pack))
        def checkMarker(failure):
            failure.trap(FirewallResult)
            self.assert_(failure.value.result == 'SPAM')
        d.addCallback(lambda _: self.assert_(False)).addErrback(checkMarker)
        return d

    def testStr(self):
        self.assertEquals('stop as spammer', str(StopFirewallStatement(stop_marker='spammer')))
        self.assertEquals('100: stop as ok', str(StopFirewallStatement(stop_marker='ok', label=100)))

class DoFirewallStatementTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.firewall.DoFirewallStatement}.
    """

    def setUp(self):
        self.message = TaggedMessage([])
        self.pack = FirewallMessagePack(self.message, getDefaultDomain())

    def testCompile1(self):
        d = DoFirewallStatement(func_name='ruleTrue', func_args={}).compile(defer.succeed(self.pack))
        def check(pack):
            self.assert_(pack is self.pack)
        d.addCallback(check)
        return d

    def testCompile2(self):
        d = DoFirewallStatement(func_name='ruleFalse', func_args={}).compile(defer.succeed(self.pack))
        def check(pack):
            self.assert_(pack is self.pack)
        d.addCallback(check)
        return d

    def testCompile3(self):
        d = DoFirewallStatement(func_name='ruleFalse', func_args={}, markers=['aaa', 'bbb']).compile(defer.succeed(self.pack))
        def check(pack):
            self.assert_(pack is self.pack)
            self.assert_(pack.message.checkHasAllTags(['aaa', 'bbb']))
        d.addCallback(check)
        return d

    def testCompile4(self):
        d = DoFirewallStatement(func_name='ruleTrue', func_args={}, markers=['aaa', 'bbb'], if_tags=['c']).compile(defer.succeed(self.pack))
        def check(pack):
            self.assert_(pack is self.pack)
            self.assert_(pack.message.checkHasNoTags(['aaa', 'bbb']))
        d.addCallback(check)
        return d

    def testStr(self):
        self.assertEquals('do ruleTrue()', str(DoFirewallStatement(func_name='ruleTrue', func_args={})))
        self.assertEquals('do ruleTrue() mark aaa, bbb', str(DoFirewallStatement(func_name='ruleTrue', func_args={}, markers=['aaa', 'bbb'])))
        self.assertEquals('do ruleTrue(a=3, b=\'ccc\') mark aaa, bbb', str(DoFirewallStatement(func_name='ruleTrue', func_args={'a' : 3, 'b' : 'ccc'}, markers=['aaa', 'bbb'])))
        self.assertEquals('100: do ruleTrue()', str(DoFirewallStatement(func_name='ruleTrue', func_args={}, label=100)))

class MessageFirewallTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.firewall.MessageFirewall}.
    """

    def testInterface(self):
        ziv.verifyClass(IMessageAnalyzer, MessageFirewall)
        ziv.verifyClass(IMessageFirewall, MessageFirewall)

    def testParse(self):
        parsed = MessageFirewall().parse('skip to 345\nif analyzed, skipped do callFunc(a=3, b="ddd") mark spam\n345: if not a, b, c stop as SPAM')
        self.assertEqual(3, len(parsed))

        self.assertEqual('skip', parsed[0].statement)
        self.assertEqual('', parsed[0].if_tags)
        self.assertEqual('345', parsed[0].skip_to_label)

        self.assertEqual('do', parsed[1].statement)
        self.assertEqual(['analyzed', 'skipped'], list(parsed[1].if_tags))
        self.assertEqual('', parsed[1].inverted_if)
        self.assertEqual('', parsed[1].label)
        self.assertEqual(['spam'], list(parsed[1].markers))
        self.assertEqual('callFunc', parsed[1].function_name)
        self.assertEqual([['a', 3], ['b', 'ddd']], list(map(lambda l: list(l), parsed[1].function_args)))

        self.assertEqual('stop', parsed[2].statement)
        self.assertEqual(['a', 'b', 'c'], list(parsed[2].if_tags))
        self.assertEqual('not', parsed[2].inverted_if)
        self.assertEqual('345', parsed[2].label)
        self.assertEqual('SPAM', parsed[2].stop_marker)

        MessageFirewall().parse('do Rule()')

    def testParseError(self):
        self.assertRaises(SyntaxError, MessageFirewall().parse, 'skip to')
        self.assertRaises(SyntaxError, MessageFirewall().parse, 'if do callFunc()')

    def testCompile(self):
        firewall = MessageFirewall()
        self.assertEqual([
                SkipFirewallStatement(skip_label=345, if_tags=None, if_inverted=False, label=None),
                DoFirewallStatement(func_name='ruleTrue', func_args={'a': 3, 'b': 'ddd'}, markers=['spam'], if_tags=['analyzed', 'skipped'], if_inverted=False, label=None),
                StopFirewallStatement(stop_marker='SPAM', if_tags=['a', 'b', 'c'], if_inverted=True, label=345)
                         ], 
                            firewall.compile(firewall.parse('skip to 345\nif analyzed, skipped do ruleTrue(a=3, b="ddd") mark spam\n345: if not a, b, c stop as SPAM')))

    def testAnalyze1(self):
        firewall = MessageFirewall()
        message = Message([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('UNKNOWN', result))

    def testAnalyze2(self):
        firewall = MessageFirewall('stop as SPAM')
        message = TaggedMessage([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('SPAM', result))

    def testAnalyze3(self):
        firewall = MessageFirewall('do ruleFalse() mark spammed\nif spammed stop as SPAM')
        message = Message([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('SPAM', result))

    def testAnalyze4(self):
        firewall = MessageFirewall('do ruleTrue() mark spammed\nif spammed stop as SPAM')
        message = TaggedMessage([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('UNKNOWN', result))

    def testAnalyze5(self):
        firewall = MessageFirewall('10: do ruleTrue()\nskip to 10')
        message = TaggedMessage([])

        def checkSkipFall(failure):
            failure.trap(errors.SkipToFallthroughError)

        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda _: self.assert_(False)).addErrback(checkSkipFall)

    def testAnalyze6(self):
        firewall = MessageFirewall('skip to 20\nstop as OK\n20: stop as SPAM')
        message = TaggedMessage([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('SPAM', result))

    def testAnalyze7(self):
        firewall = MessageFirewall('do ruleTrue() mark xxx\nif xx stop as A\nstop as B')
        message = TaggedMessage([])
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('B', result))

    def testSetRules(self):
        firewall = MessageFirewall()
        message = TaggedMessage([])
        firewall.setRules('stop as NEW')
        return firewall.analyze(message, getDefaultDomain()).addCallback(lambda result: self.assertEquals('NEW', result))

    def testGetRules(self):
        firewall = MessageFirewall()
        self.assertEquals('', firewall.getRules())

        firewall = MessageFirewall('stop as X')
        self.assertEquals('stop as X', firewall.getRules())

    def testSyntaxCheck(self):
        firewall = MessageFirewall()

        firewall.syntaxCheck('stop as Y')
        self.assertRaises(SyntaxError, firewall.syntaxCheck, 'XXXX')

    def testDebug(self):
        firewall = MessageFirewall('do ruleTrue() mark xxx\nif not xxx do ruleFalse() mark zzz\nskip to 100\n200: stop as C\n100: if yyyy stop as D\nif xx stop as A\nstop as B')
        message = TaggedMessage([])
        
        def logCallback(log):
            self.fwLog = log

        return firewall.analyze(message, getDefaultDomain(), debug=True, logCallback=logCallback).addCallback(lambda _: self.assertEquals(
                    [
                     '[ENTER]: do ruleTrue() mark xxx',
                     'Result: True',
                     '[ENTER]: if not xxx do ruleFalse() mark zzz',
                     'Result: False',
                     "Tagged message with tags: ['zzz'], current tags are: ['zzz']",
                     '[ENTER]: skip to 100',
                     'Skipping to 100',
                     "Labels for skip don't match 100 != 200",
                     'Stopped skip to at label 100',
                     '[ENTER]: 100: if yyyy stop as D',
                     '[ENTER]: if xx stop as A',
                     '[ENTER]: stop as B',
                     'Stopping firewall with result: B']
               , self.fwLog))

    def testPickling(self):
        import pickle

        fw = MessageFirewall()
        self.assertEquals('', pickle.loads(pickle.dumps(fw)).getRules())

        fw.setRules('stop as OK')
        self.assertEquals('stop as OK', pickle.loads(pickle.dumps(fw)).getRules())
