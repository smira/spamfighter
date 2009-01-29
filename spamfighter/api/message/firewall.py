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
Команды C{sf.message.firewall.*}.
"""

import types
from zope.interface import implements
from twisted.internet import defer

from spamfighter.core.commands import ICommand, install, DomainedCommand, errors
from spamfighter.core.domain import DomainKeyError
from spamfighter.interfaces import IMessageFirewall
from spamfighter.core.firewall import SyntaxError

class FirewallCommand(DomainedCommand):
    """
    Базовая команда работы с firewall

    @ivar firewall: найденный в домене firewall
    @type firewall: L{IMessageFirewall}
    """
    commandSignature = {
            'firewall' : { 'type' : types.StringType, 'required' : True, }
                       }

    def init(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.
        """
        def doIt(_):
            try:
                self.firewall = self.domain.get(self.params.firewall)
            except DomainKeyError:
                raise errors.AttributeKeyException, self.params.firewall

            if not IMessageFirewall.providedBy(self.firewall):
                raise errors.NotAFirewallError, self.params.firewall

        return defer.maybeDeferred(super(FirewallCommand, self).init).addCallback(doIt)

class FirewallRulesGetCommand(FirewallCommand):
    """
    Реализация команды C{sf.message.firewall.rules.get}.
    """
    implements(ICommand)

    commandName = 'sf.message.firewall.rules.get'
    commandSignature = {
                       }
    resultSignature = {
            'rules' : { 'type' : types.StringType, 'required' : True, }
                      }

    install()

    def perform(self):
        self.result.rules = self.firewall.getRules()

class FirewallRulesSetCommand(FirewallCommand):
    """
    Реализация команды C{sf.message.firewall.rules.set}.
    """
    implements(ICommand)

    commandName = 'sf.message.firewall.rules.set'
    commandSignature = {
            'rules' : { 'type' : types.StringType, 'required' : True, }
                       }
    resultSignature = {
                      }

    install()

    def perform(self):
        try:
            self.firewall.setRules(self.params.rules)
        except SyntaxError, message:
            raise errors.FirewallSyntaxError(message)

class FirewallRulesCheckCommand(FirewallCommand):
    """
    Реализация команды C{sf.message.firewall.rules.check}.
    """
    implements(ICommand)

    commandName = 'sf.message.firewall.rules.check'
    commandSignature = {
            'rules' : { 'type' : types.StringType, 'required' : True, }
                       }
    resultSignature = {
                      }

    install()

    def perform(self):
        try:
            self.firewall.syntaxCheck(self.params.rules)
        except SyntaxError, message:
            raise errors.FirewallSyntaxError(message)
