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
Атрибуты сообщений и их домены.
"""

from zope.interface import implements
from spamfighter.interfaces import IAttribute, IAttributeDomain 
from netaddr import IP

class AttributeNotFoundError(Exception):
    """
    Атрибут по имени не был обнаружен.
    """

class AttributeDomain(object):
    """
    Домент (тип атрибута).

    @ivar _name: имя атрибута
    @type _name: C{str}
    """
    implements(IAttributeDomain)

    def __init__(self, name):
        """
        Конструктор.

        @param name: имя атрибута
        @type name: C{str}
        """
        self._name = name

    def name(self):
        """
        Получить имя атрибута.

        @return: имя атрибута
        @rtype: C{str}
        """
        return self._name

    def serialize(self, attribute):
        """
        Получить сериализованное значение атрибута.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        raise NotImplementedError, self

    def deserialize(self, value):
        """
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        raise NotImplementedError, self

    def __eq__(self, other):
        return isinstance(other, AttributeDomain) and self._name == other._name

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._name)

class TextAttributeDomain(AttributeDomain):
    """
    Тип атрибута "текст сообщения". Основной тип атрибутов при анализе сообщений.
    """

    def serialize(self, attribute):
        """
        Получить сериализованное значение атрибута.

        Сериализованное представление - это всегда строка в utf-8.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        if isinstance(attribute.value(), unicode):
            return attribute.value().encode('utf-8')

        return attribute.value()

    def deserialize(self, value):
        """
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        if isinstance(value, unicode):
            return Attribute(self, value)

        return Attribute(self, value.decode('utf-8').strip())

class IPAttributeDomain(AttributeDomain):
    """
    Атрибут, в котором хранится IP.
    """
    def serialize(self, attribute):
        """
        Получить сериализованное значение атрибута.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """

        return str(attribute.value())

    def deserialize(self, value):
        """
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """

        return Attribute(self, IP(value))

class IntAttributeDomain(AttributeDomain):
    """
    Тип атрибута "целое число".
    """

    def serialize(self, attribute):
        """
        Получить сериализованное значение атрибута.

        Сериализованное представление - это всегда число

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """
        if not isinstance(attribute.value(), (int, long)):
            raise TypeError(attribute.value());

        return attribute.value()

    def deserialize(self, value):
        """
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """
        if not isinstance(value, (int, long)):
            raise TypeError(value);

        return Attribute(self, value)

class UniqueIntAttributeDomain(IntAttributeDomain):
    """
    Уникальный атрибут, тип "целое число".
    """

class Attribute(object):
    """
    Атрибуты характеризуют отправителя и получателя сообщений, они могут нести разную информацию.

    Атрибут является частью сообщения (L{IMessage}), тип атрибута (L{IAttributeDomain}) - его свойством.

    @ivar _domain: домен атрибута
    @type _domain: L{IAttributeDomain}
    @ivar _value: значение атрибута
    """
    implements(IAttribute)

    def __init__(self, domain, value):
        """
        Конструктор.

        @ivar domain: домен атрибута
        @type domain: L{IAttributeDomain}
        @ivar value: значение атрибута
        """
        self._domain = domain
        self._value = value

    def domain(self):
        """
        Получить домен атрибута.

        @return: домен атрибута
        @rtype: L{IAttributeDomain}
        """
        return self._domain

    def value(self):
        """
        Получить значение атрибута.

        @return: значение атрибута
        """
        return self._value

    def serialize(self):
        """
        Получить сериализованное значение атрибута.

        @return: сериализованное значение атрибута
        """
        return self._domain.serialize(self)

    def __eq__(self, other):
        return isinstance(other, Attribute) and self._domain is other._domain and self._value == other._value

    def __repr__(self):
        return "Attribute(%r, %r)" % (self._domain, self._value)

