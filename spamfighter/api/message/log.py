# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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


