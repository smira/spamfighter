# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.message.input} - анализ входящего сообщения.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, DomainedCommand
from spamfighter.core.message import ITransitMessage

class MessageInputCommand(DomainedCommand):
    """
    Реализация команды C{sf.message.input}.
    """
    implements(ICommand)

    commandName = 'sf.message.input'
    commandSignature = {
            'message' : { 'type' : ITransitMessage, 'required' : True, },
            'debug'   : { 'type' : types.BooleanType, 'required' : False, }
                       }
    resultSignature = {
            'result' : { 'type' : types.StringType, 'required' : True, },
            'log' : { 'type' : types.StringType, 'required' : False, }
                      }

    install()

    def perform(self):
        message = self.params.message.getMessage(self.domain)
        analyzer = self.domain.get('messageAnalyzer')

        def gotResult(result):
            self.result.result = result

        def logCallback(log):
            self.result.log = "\n".join(log)

        return analyzer.analyze(message, self.domain, self.params.debug, logCallback).addCallback(gotResult)
