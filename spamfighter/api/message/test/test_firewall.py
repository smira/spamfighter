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
Тесты на L{spamfighter.api.message.firewall}.
"""

from twisted.trial import unittest
from zope.interface import implements

from spamfighter.core.commands import ICommand
from spamfighter.api.message.firewall import FirewallCommand, FirewallRulesGetCommand, FirewallRulesSetCommand, FirewallRulesCheckCommand
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.firewall import MessageFirewall

class FakeFirewallCommand(FirewallCommand):
    implements(ICommand)

    commandName = 'sf.test.firewall'

    commandSignature = {
                       }

    resultSignature  = {
                       }

    def perform(self):
        return None

class FirewallCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallCommand}.
    """

    def setUp(self):
        self.c = FakeFirewallCommand()
        self.firewall = MessageFirewall()
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testNoSuchFirewall(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'noSuchFirewall'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AttributeKeyException'))

    def testNotAFirewall(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'messageDomain'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.NotAFirewallError'))

    def testGetFirewall(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL'})
        return self.c.run().addCallback(lambda _: self.assert_(self.c.firewall is self.firewall))

class FirewallRulesGetCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesGetCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesGetCommand()
        self.firewall = MessageFirewall('stop as SPAMMER')
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as SPAMMER', self.c.result.rules))

class FirewallRulesSetCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesSetCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesSetCommand()
        self.firewall = MessageFirewall()
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL', 'rules' : 'stop as TEST'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as TEST', self.firewall.getRules()))

    def testRun(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL', 'rules' : 'YYYY'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.FirewallSyntaxError'))

class FirewallRulesCheckCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesCheckCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesCheckCommand()
        self.firewall = MessageFirewall('stop as SPAM')
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL', 'rules' : 'stop as TEST'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as SPAM', self.firewall.getRules()))

    def testRun(self):
        self.c.params.getUnserialized({'partner' : None, 'firewall' : 'testFIREWALL', 'rules' : 'YYYY'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.FirewallSyntaxError'))
