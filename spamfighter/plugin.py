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
Подсистема плагинов СпамоБорца и интерфейсы плагинов.
"""

from twisted.plugin import getPlugins

from zope.interface import Interface

class INamedPlugin(Interface):
    """
    Базовый интерфейс плагинов: плагин, который имеет имя.
    """

    def name():
        """
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """

class IDefaultDomainProvider(INamedPlugin):
    """
    Интерфейс плагина, возвращающего ссылку на провайдер домена по умолчанию. 
    """

    def getDefaultDomain():
        """
        Получить домен по умолчанию в системе.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IDomain}
        """

class IPartnerAuthorizerProvider(INamedPlugin):
    """
    Интерфейс плагина, возвращающего ссылку на механизм авторизации партнеров. 
    """

    def getPartnerAuthorizer():
        """
        Получить механизм авторизации партнеров.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
        """

class PluginNotFoundError(Exception):
    """
    Не найден плагин с указанным именем.
    """

class PluginAmbiguityError(Exception):
    """
    Найдено более одного плагина с указанным именем.
    """

def loadPlugin(interface, name, package = None):
    """
    Загрузить указанный плагин СпамоБорца. Возвращает
    экземлпяр объекта плагина.

    @param interface: интерфейс, который должен реализовывать плагин
    @param name: имя плагина (см. L{INamedPlugin})
    @type name: C{str}
    """
    if package == None:
        import spamfighter.plugins
        package = spamfighter.plugins

    plugins = filter(lambda plugin: plugin.name() == name, getPlugins(interface, package))

    if len(plugins) == 0:
        raise PluginNotFoundError, name

    if len(plugins) > 1:
        raise PluginAmbiguityError, name

    return plugins[0]
