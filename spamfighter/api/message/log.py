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
Команды C{sf.message.log.*}.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, DomainedCommand, errors, Array
from spamfighter.core.domain import DomainKeyError
from spamfighter.interfaces import IMessageLog, ILogEntry
from spamfighter.core.firewall import SyntaxError

class MessageLogFetchCommand(DomainedCommand):
    """
    Команда C{sf.message.log.fetch}.

    Получить сообщения из лога сообщений.
    """
    implements(ICommand)

    commandName = 'sf.message.log.fetch'

    commandSignature = {
            'first' : { 'type' : types.IntType, 'required' : False, },
            'last'  : { 'type' : types.IntType, 'required' : False, },
            'firstID'  : { 'type' : types.IntType, 'required' : False, },
            'log' : { 'type' : types.StringType, 'required' : True, }
                      }

    resultSignature = {
            'entries' : { 'type' : Array(ILogEntry), 'required' : True, }
                       }

    install()

    def perform(self):
        try:
            log = self.domain.get(self.params.log)
        except DomainKeyError:
            raise errors.AttributeKeyException, self.params.log

        if not IMessageLog.providedBy(log):
            raise errors.NotAMessageLogError, self.params.log

        def gotEntries(entries):
            self.result.entries = entries

        return log.fetch(first=self.params.first, last=self.params.last, firstID=self.params.firstID).addCallback(gotEntries)


