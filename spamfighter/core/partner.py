# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Базовые классы и методы работы с партнерами.
"""

from spamfighter.plugin import loadPlugin, IPartnerAuthorizerProvider
from spamfighter.utils import config

class PartnerAuthorizationFailedError(Exception):
    """
    Авторизация партнера была неуспешной.
    """

defaultPartnerAuthorizer = None

def getPartnerAuthorizer():
    """
    Получить текущий механизм авторизации партнеров.

    @return: механизм авторизации партнеров
    @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
    """
    global defaultPartnerAuthorizer

    if defaultPartnerAuthorizer is None:
        defaultPartnerAuthorizer = getPartnerAuthorizerProvider().getPartnerAuthorizer()

    return defaultPartnerAuthorizer

defaultPartnerAuthorizerProvider = None

def getPartnerAuthorizerProvider():
    """
    Получить провайдер авторизации партнеров.

    Загружаем как плагин, предсоставляющий интерфейс L{IPartnerAuthorizerProvider} с именем 
    из конфига: config.plugins.partner.default_provider

    @return: провайдер авторизации партнеров
    @rtype: L{IPartnerAuthorizerProvider}
    """
    global defaultPartnerAuthorizerProvider

    if defaultPartnerAuthorizerProvider is None:
        defaultPartnerAuthorizerProvider = loadPlugin(IPartnerAuthorizerProvider, config.plugins.partner.default_provider)

    return defaultPartnerAuthorizerProvider
