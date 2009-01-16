# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.domain.list} - получение списка имён свойств домена.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, DomainedCommand, Array

class DomainListCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.list}.
    """
    implements(ICommand)

    commandName = 'sf.domain.list'
    commandSignature = {
                       }
    resultSignature = {
            'properties' : { 'type' : Array(types.StringType), 'required' : True, }
                      }

    install()

    def perform(self):
        self.result.properties = self.domain.list()
