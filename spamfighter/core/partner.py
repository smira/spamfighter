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
