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
Тесты на L{spamfighter.core.commands.dispatcher}.
"""

from twisted.trial import unittest

from spamfighter.core.commands import errors
from spamfighter.core.commands.command import Command
from spamfighter.core.commands.dispatcher import dispatchCommand, installCommand, deinstallCommand

class FakeCommand(Command):
    commandName = "sf.test.fake"
    commandSignature = {}
    resultSignature = {}

class CommandDispatchTestCase(unittest.TestCase):
    """
    Тестируем диспетчеризацию комманд.
    """

    def testDispatchAbsent(self):
        self.assertRaises(errors.CommandUnknownException, dispatchCommand, 'sf.test.absent')

    def testDispatchOK(self):
        installCommand(FakeCommand)
        self.assert_(type(dispatchCommand('sf.test.fake')) is FakeCommand)
        deinstallCommand(FakeCommand)

    def testDoubleInstall(self):
        installCommand(FakeCommand)
        self.assertRaises(AssertionError, installCommand, FakeCommand)
        deinstallCommand(FakeCommand)

