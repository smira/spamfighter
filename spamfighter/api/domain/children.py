# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.domain.children} - получение списка имён поддоменов.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, DomainedCommand, Array

class DomainChildrenCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.children}.
    """
    implements(ICommand)

    commandName = 'sf.domain.children'
    commandSignature = {
                       }
    resultSignature = {
            'children' : { 'type' : Array(types.StringType), 'required' : True, }
                      }

    install()

    def perform(self):
        def gotChildren(children):
            self.result.children = children.keys()

        return self.domain.children().addCallback(gotChildren)
