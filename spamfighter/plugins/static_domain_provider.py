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
Плагин, реализующий статический домен по умолчанию.

В частности, он реализует самый простой - пустой домен по умолчанию
"""

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.plugin import IDefaultDomainProvider
from spamfighter.core.domain import BaseDomain

class StaticDefaultDomainProvider(object):
    """
    Провайдер статического дефолтного домена.
    """
    implements(IPlugin, IDefaultDomainProvider)

    def __init__(self, name, dict, parent=None):
        """
        Конструктор.

        @param name: имя плагина-домена
        @type name: C{str}
        @param dict: содержимое домена
        @type dict: C{dict}
        """
        self._name = name
        self.domain = BaseDomain(dict=dict, key=name, parent=parent)

    def name(self):
        """
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return self._name

    def getDefaultDomain(self):
        """
        Получить домен по умолчанию в системе.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IDomain}
        """
        return self.domain

emptyDomainProvider = StaticDefaultDomainProvider('EmptyDefaultDomainProvider', {})

from spamfighter.core.message import MessageDomain, TextAttributeDomain, UniqueIntAttributeDomain, IPAttributeDomain
from spamfighter.core.firewall import MessageFirewall

defaultDomainProvider = StaticDefaultDomainProvider('DefaultDefaultDomainProvider', {
        'messageDomain' : MessageDomain(TextAttributeDomain('text'), UniqueIntAttributeDomain('from'), IPAttributeDomain('ip')),
        'messageAnalyzer' : MessageFirewall(),
    })

emptySubDomainProvider = StaticDefaultDomainProvider('EmptySubDefaultDomainProvider', {}, parent=defaultDomainProvider.getDefaultDomain())
