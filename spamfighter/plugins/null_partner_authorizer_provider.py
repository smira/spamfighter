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
Плагин, реализующий авторизацию партнеров без логинов/паролей (доверительный вариант).
"""

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.plugin import IPartnerAuthorizerProvider
from spamfighter.core.null_partner import NullPartnerAuthorizer

class NullPartnerAuthorizerProvider(object):
    """
    Провайдер авторизации партнеров без логинов/паролей.
    """
    implements(IPlugin, IPartnerAuthorizerProvider)

    def __init__(self):
        """
        Конструктор.
        """

    def name(self):
        """
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return 'NullPartnerAuthorizerProvider'

    def getPartnerAuthorizer(self):
        """
        Получить механизм авторизации партнеров.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
        """
        return NullPartnerAuthorizer()

nullPartnerAuthorizer = NullPartnerAuthorizerProvider()

