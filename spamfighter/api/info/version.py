# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.info.version} - получение версии сервера
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, Command
from spamfighter import version

class InfoVersionCommand(Command):
    """
    Реализация команды C{sf.info.version}.
    """
    implements(ICommand)

    commandName = 'sf.info.version'
    commandSignature = {
                       }
    resultSignature = {
            'version' : { 'type' : types.StringType, 'required' : True, }
                      }

    install()

    def perform(self):
        self.result.version = version

