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
Тесты на L{spamfighter.core.commands.partner}.
"""

from twisted.trial import unittest
from zope.interface import implements

from spamfighter.interfaces import IPartner, IDomain
from spamfighter.core.commands import command
from spamfighter.core.commands.partner import PartneredCommand, DomainedCommand

class FakePartneredCommand(PartneredCommand):
    implements(command.ICommand)

    commandName = 'sf.test.partnered'

    commandSignature = {
                       }

    resultSignature  = {
                       }

    def perform(self):
        return None

class FakeDomainedCommand(DomainedCommand):
    implements(command.ICommand)

    commandName = 'sf.test.domained'

    commandSignature = {
                       }

    resultSignature  = {
                       }

    def perform(self):
        return None

class PartneredCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.partner.PartneredCommand}.
    """

    def setUp(self):
        self.c = FakePartneredCommand()

    def testAuthOK(self):
        self.c.params.getUnserialized({'partner' : None})
        return self.c.run().addCallback(lambda _: self.assert_(IPartner.providedBy(self.c.partner)))

    def testAuthFail(self):
        self.c.params.getUnserialized({'partner' : 111})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AuthorizationFailedException'))

class DomainedCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.partner.DomainedCommand}.
    """

    def setUp(self):
        self.c = FakeDomainedCommand()

    def testDomainOk(self):
        self.c.params.getUnserialized({'partner' : None})
        return self.c.run().addCallback(lambda _: self.assert_(IPartner.providedBy(self.c.partner))).addCallback(lambda _: self.assert_(IDomain.providedBy(self.c.domain)))

    def testDomainFail(self):
        self.c.params.getUnserialized({'partner' : None, 'domain' : 'no/such/domain'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.DomainPathNotFoundException'))
