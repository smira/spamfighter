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
Поддержка сериализации/десериализации для типов данных, передаваемых в командах.
"""

from zope.interface import Interface

from spamfighter.utils.registrator import registrator

class ISerializable(Interface):
    """
    Сущность, которая может передаваться в команде (и, соответственно, должна 
    уметь превращаться в часть параметров или результатов) и умеет "вылезать"
    из неё.
    """

    def serialize():
        """
        Получить сериализованное представление элемента.

        @return: сериализованное представление, Deferred (C{str})
        @rtype: L{twisted.internet.defer.Deferred}
        """

    def unserialize(serialized):
        """
        Восстановить экземпляр объекта из его сериализованного представления

        @param serialized: сериализованное представление объекта
        @return: восстановленный экземпляр объекта
        """

serializers = {}

class SerializerNotFoundException(Exception):
    """
    Не был найден подходящий десериализатор для переданного интерфейса.
    """

@registrator
def register_serializer(cls, interface):
    """
    Регистрируем класс, который занимается сериализацией интерфейса.

    @param interface: сериализуемый интерфейс
    @type interface: L{ISerializable}
    @param serializer: класс, который умеет рассериализовывать объекты для переданного интерфейса
    """
    serializers[interface] = cls

def get_serializer(interface):
    """
    Получить класс, который занимается сериализацией для интерфейса.

    @param interface: сериализуемый интерфейс
    @type interface: L{ISerializable}
    @rtype: L{ISerializable}
    """
    if not serializers.has_key(interface):
        raise SerializerNotFoundException(str(interface))
    return serializers[interface]


import datetime
from time import strptime

class DateTime(datetime.datetime):
    """
    Наследник datetime.datetime, который требует в конструктор 
    строку в формате ISO 8601 и при вызове str сериализуется 
    также в формат ISO 8601.
    """

    def __init__(self, str):
        """
        @param str: Строка с датой в формате ISO 8601
        @type str: C{str}
        """
        datetime.datetime.__init__(self, *strptime(str, "%Y%m%dT%H:%M:%S")[0:6])

    def __str__(self):
        return self.strftime("%Y%m%dT%H:%M:%S")

    @staticmethod
    def toISO(date):
        if type(date) == type(None):
            return None
        return date.strftime("%Y%m%dT%H:%M:%S")

    @staticmethod
    def fromISO(str):
        return datetime.datetime(*strptime(str, "%Y%m%dT%H:%M:%S")[0:6])
