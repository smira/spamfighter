# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
