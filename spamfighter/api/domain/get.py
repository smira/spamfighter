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


