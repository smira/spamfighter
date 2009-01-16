# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
