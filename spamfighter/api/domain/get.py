# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.domain.get} - получение информации об одном свойстве домена.
"""

import types
from zope.interface import implements, providedBy

from spamfighter.core.commands import ICommand, install, DomainedCommand, Array, errors
from spamfighter.core.domain import DomainKeyError

class DomainGetCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.get}.
    """
    implements(ICommand)

    commandName = 'sf.domain.get'
    commandSignature = {
            'name' : { 'type' : types.StringType, 'required' : True }
                       }
    resultSignature = {
            'repr'       : { 'type' : types.StringType, 'required' : True, },
            'interfaces' : { 'type' : Array(types.StringType), 'required' : True, },
            'classname'  : { 'type' : types.StringType, 'required' : True, }
                      }

    install()

    def perform(self):
        try:
            value = self.domain.get(self.params.name)
        except DomainKeyError:
            raise errors.AttributeKeyException, self.params.name

        self.result.repr = str(value)
        self.result.classname = value.__class__.__name__
        self.result.interfaces = map(lambda iface: iface.__name__, providedBy(value))


