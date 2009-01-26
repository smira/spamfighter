# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
