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
