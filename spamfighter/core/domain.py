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
Реализация основных классов доменов.
"""

import hashlib
from zope.interface import implements
from twisted.internet import defer

from spamfighter.interfaces import IDomain, IDomainBindable
from spamfighter.plugin import loadPlugin, IDefaultDomainProvider
from spamfighter.utils import config

class DomainKeyError(Exception):
    """
    В данном домене нет указанного значения.
    """

class DomainPathError(Exception):
    """
    Указанный путь в поддоменах отсутствует.
    """

class DomainDuplicateError(Exception):
    """
    У данного домена уже есть поддомен с таким же именем.
    """

class BaseDomain(object):
    """
    Домен - единица настроек, привязки локальных элементов 
    внутренного устройства СпамоБорца. 
    
    Все домены связаны в дерево, начинающееся главным доменом 
    (глобально известным серверу).

    Базовый класс доменов представляет домены "в памяти", без какого-либо 
    сохранения, а также без "детей".

    @ivar _name: имя домена
    @type _name: C{str}
    @ivar _key: ключ домена
    @type _key: C{str}
    @ivar _parent: предок данного домена
    @type _parent: L{IDomain}
    @ivar _dict: хеш (словарь) атрибутов, заданных в данном домене
    @type _dict: C{dict}
    @ivar _children: хэш поддоменов по их именам
    @type _children: C{dict}
    """
    implements(IDomain)

    def __init__(self, key=None, name=None, parent=None, dict=None):
        """
        Конструктор.

        @param parent: предок текущего домена
        @type parent: L{IDomain}
        @param dict: начальное значение домена
        @type dict: C{dict}
        """
        assert key is not None or (name is not None and parent is not None)

        self._parent = parent

        if key is not None:
            self._key = key
        else:
            self._key = hashlib.md5(self._parent.key() + name).hexdigest()
        self._name = name
        self._children = {}

        self._dict = {}
        if dict is not None:
            self._dict = dict.copy()
            for property, value in self._dict.iteritems():
                if IDomainBindable.providedBy(value):
                    value.bind(self, property)

    def name(self):
        """
        Имя домена (относительно пути).

        Если домен корневой или не содержится в пути,
        имя может быть C{None}.

        @return: имя домена
        @rtype: C{str}
        """
        return self._name

    def key(self):
        """
        Ключ домена. Уникальное и постоянное свойство
        каждого домена.

        @return: ключ домена
        @rtype: C{str}
        """
        return self._key

    def parent(self):
        """
        Получить предка данного домена.

        Если предка нет, будет возвращено C{None}.

        @rtype: L{IDomain}
        """
        return self._parent

    def children(self):
        """
        Получить список "дочерних" доменов.

        @return: Deferred, результат - хэш (имя домена: домен) (C{dict(}L{IDomain}C{)})
        @rtype: C{twisted.internet.defer.Deferred}
        """
        return defer.succeed(self._children)

    def createSubdomain(self, name):
        """
        Создать дочерний поддомен.

        @param name: имя поддомена
        @type name: C{str}
        @return: Deferred с созданным поддоменом, L{IDomain}
        @rtype: C{twisted.internet.defer.Deferred}
        @raise DomainDuplicateError: два поддомена с одинаковым именем не могут существовать
        """
        if name in self._children:
            return defer.fail(DomainDuplicateError(name))

        domain = BaseDomain(parent=self, name=name)
        self._children[name] = domain
        return defer.succeed(domain)

    def walk(self, path):
        """
        "Пройти" по пути от текущего домена.

        @param path: путь относительно текущего домена, строка со слэшами
        @type path: C{str}
        @return: Deferred, найденный домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred}
        @raise DomainPathError: домен не найден
        """

        def _walk(domain, components):
            if len(components) == 0:
                return defer.succeed(domain)
            component = components.pop(0)

            if component == '':
                return _walk(domain, components)

            def gotChildren(children):
                if not children.has_key(component):
                    raise DomainPathError, path

                return _walk(children[component], components)

            return domain.children().addCallback(gotChildren)

        components = path.split('/')
        return _walk(self, components)

    def get(self, property):
        """
        Получить значение свойства домена.

        Если текущий домен не содержит информацию о данном свойстве, будет
        предпринято обращение к предку домена за данным свойством.

        @param property: имя свойства
        @type property: C{str}
        @return: значение свойства
        """
        if self._dict.has_key(property):
            return self._dict[property]

        if self._parent is not None:
            return self._parent.get(property)

        raise DomainKeyError, property

    def has(self, property):
        """
        Есть ли у домена указанное свойство?

        @param property: имя свойства
        @type property: C{str}
        @rtype: C{bool}
        """
        return property in self._dict

    def delete(self, property):
        """
        Удалить свойство из домена.

        При следующем обращении к свойству оно будет получено через предка домена,
        т.е. это эквивалентно сбросу на "значение по умолчанию".

        @param property: имя свойства
        @type property: C{str}
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """
        if self._dict.has_key(property):
            del self._dict[property]

        return defer.succeed(None)

    def set(self, property, value):
        """
        Установить значение свойства в домене.

        Данный метод может также создать свойство, если оно ранее не существовало 
        и переопределить свойство домена-предка.

        @param property: имя свойства
        @type property: C{str}
        @param value: значение свойства
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """
        try:
            if IDomainBindable.providedBy(value):
                value.bind(self, property)
            self._dict[property] = value
        except:
            return defer.fail()

        return defer.succeed(None)

    def list(self):
        """
        Получить список имён свойств домена.

        @return: список имён свойств
        @rtype: C{list(str)}
        """
        return self._dict.keys()

def getDefaultDomain():
    """
    Получить домен по умолчанию, который является предком всех доменов.

    Получаем через провайдер домена по умолчанию.

    @return: домен по умолчанию
    @rtype: L{IDomain}
    """
    return getDefaultDomainProvider().getDefaultDomain()

defaultDomainProvider = None

def getDefaultDomainProvider():
    """
    Получить провайдер домена по умолчанию.

    Загружаем как плагин, предсоставляющий интерфейс L{IDefaultDomainProvider} с именем 
    из конфига: config.plugins.domain.default_provider

    @return: провайдер домена по умолчанию
    @rtype: L{IDefaultDomainProvider}
    """
    global defaultDomainProvider

    if defaultDomainProvider is None:
        defaultDomainProvider = loadPlugin(IDefaultDomainProvider, config.plugins.domain.default_provider)

    return defaultDomainProvider

