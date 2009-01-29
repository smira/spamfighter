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
Модуль авторизации партнеров без логинов/паролей (на доверии).
"""

from zope.interface import implements
from twisted.internet import defer

from spamfighter.interfaces import IPartner, IPartnerAuthorizer
from spamfighter.core.partner import PartnerAuthorizationFailedError
from spamfighter.core.domain import getDefaultDomain, BaseDomain
from spamfighter.plugin import loadPlugin, IDefaultDomainProvider
from spamfighter.utils import config

class NullPartner(object):
    """
    Партнер, авторизованный без логина/пароля (на доверии).

    @ivar domain: корневой домен партнера
    @type domain: L{BaseDomain}
    """
    implements(IPartner)

    def __init__(self):
        """
        Конструктор.
        """
        domainProvider = loadPlugin(IDefaultDomainProvider, config.plugins.domain.null_partner_domain_provider)
        self.domain = domainProvider.getDefaultDomain()

    def rootDomain(self):
        """
        Получить корневой домен партнера.

        @return: Deferred, корневой домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred} 
        """
        return defer.succeed(self.domain)

class NullPartnerAuthorizer(object):
    """
    Провайдер авторизации партнеров без логина/пароля (на доверии).

    В этой ситуации доступ к СпамоБорцу ограничен с помощью других средств
    (HTTP-proxy, firewall).

    @ivar partner: единственный партнер, который обеспечивает весь доступ
    @type partner: L{NullPartner}
    """
    implements(IPartnerAuthorizer)

    def __init__(self):
        """
        Конструктор.
        """
        self.partner = NullPartner()

    def authorize(self, partner_info):
        """
        Выполнить авторизацию партнера.

        @param partner_info: информация о партнере
        @return: Deferred, партнер (L{IPartner})
        @rtype: C{twisted.internet.defer.Deferred} 
        """
        if partner_info is not None:
            return defer.fail(PartnerAuthorizationFailedError())

        return defer.succeed(self.partner)
