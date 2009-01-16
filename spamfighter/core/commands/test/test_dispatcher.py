# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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

