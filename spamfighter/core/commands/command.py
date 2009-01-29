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
Базовый класс команды API.
"""

import datetime
import types
import sys

from zope.interface import Interface, Attribute
from twisted.internet import defer
from twisted.python import failure

from spamfighter.core.commands.serialize import ISerializable, DateTime, get_serializer
from spamfighter.core.commands import errors

class Array(object):
    """
    Виртуальный тип данных "массив" для сигнатуры команд.

    Массив содержит тип данных элемента.
    """
    def __init__(self, elementType):
        self.elementType = elementType

class ICommand(Interface):
    """
    Интерфейс команд. Этот интерфейс обязаны реализовывать
    все наследники Command.
    """

    commandName = Attribute("""Имя команды""")
    commandSignature = Attribute("""Сигнатура параметров команды""")
    resultSignature = Attribute("""Сигнатура возвращаемого результата""")

    def perform(self):
        """
        Выполнить команду. Выполняет действия по вычислению результата
        команды. Перед вызовом проверяется наличие всех обязательных 
        параметров.

        @rtype: L{twisted.internet.defer.Deferred}
        @return: Deferred, которая вызывается после завершения вычисления команды. Если
                 команда была успешна, то в массив C{result} команды должен быть записан результат.
        """

class Command(object):
    """
    Базовый класс для всех команд.

    Любой производный класс должен быть отнаследован от этого класса
    и должен реализовывать интерфейс L{ICommand}.

    @ivar _params: параметры команды (исходный словарь)
    @type _params: C{dict}
    @ivar _result: результат команды (исходный словарь)
    @type _result: C{dict}
    @ivar params: обертка над параметрами
    @type params: L{_ParamsWrapper}
    @ivar result: обертка над результатом
    @type result: L{_ParamsWrapper}
    """

    class _ParamsWrapper(object):
        """Класс-обертка для проверки корректности
        сигнатуры параметров или результата команды.
        """

        def __init__(self, signature, holder):
            """Констуктор.

            @param signature: сигнатура параметров
            @type signature: хеш имя_параметра -> информация о типе параметра и т.п.
            @param holder: ссылка на переменную, в которой будут храниться сами проверяемые значения
            @type holder: C{dict}
            """
            self._signature = signature
            self._holder = holder

        def __setattr__(self, param, value):
            def checkType(_type, value):
                """
                Проверить тип, что тип значения совместим с типом в сигнатуре команды
                """

                if type(_type) is Array:
                    if not issubclass(type(value), types.ListType):
                        raise TypeError, param
                    for val in value:
                        checkType(_type.elementType, val)
                elif issubclass(_type, Interface):
                    if not _type.providedBy(value):
                        raise TypeError, param
                    if not ISerializable.providedBy(value):
                        raise TypeError, param
                elif _type is long and type(value) is int:
                    pass
                elif not isinstance(value, _type):
                    raise TypeError, param

            if param == "_signature" or param == "_holder":
                object.__setattr__(self, param, value)
                return

            if param not in self._signature:
                raise AttributeError, param

            checkType(self._signature[param]['type'], value)

            self._holder[param] = value

        def __getattr__(self, param):
            if param not in self._signature:
                raise AttributeError, param

            if param not in self._holder:
                if self._signature[param]['required']:
                    raise AttributeError, param
                return None

            return self._holder[param]

        def checkSignature(self):
            """
            Проверить установленность всех необходимых параметров.

            @raise AttributeError: если какой-то обязательный параметр не задан.
            """
            for param in self._signature:
                if self._signature[param]["required"] and param not in self._holder:
                    raise AttributeError, param

        def getSerialized(self):
            """
            Получить сериализованное (до хеша) представление 
            массива.

            @return: Deferred (C{dict})
            @rtype: L{twisted.internet.defer.Deferred}
            """

            def placerHash(result, param):
                """
                Построить function closure, которая добавляет элемент
                в хеш C{result} по ключу C{param} и возвращает ссылку 
                на добавленный элемент. 
                """
                def curried(val):
                    result[param] = val
                    return result[param]

                return curried

            def placerList(result):
                """
                Построить function closure, которая добавляет элемент
                в массив C{result} и возвращает ссылку на добавленный элемент. 
                """

                def curried(val):
                    result.append(val)
                    return result[len(result)-1]

                return curried

            def serializeValue(placer, _type, value):
                """
                Сериализовать одно значение.

                Если значение является простым типом, оно записывается в результат.
                Если значение является объектом, поддерживающим интерфейс L{ISerializable}, 
                то значением становится сериализованный объект.
                Если значение является массивом, его значением является массив сериализованных
                элементов.

                @param placer: функция, которая обеспечивает помещение сериализованного значения в результат
                @type placer: C{function(value)}
                @param _type: тип сериализуемого элемента
                @param value: сериализуемое значение
                @return: список L{twisted.internet.defer.Deferred}, по завершении которых результат будет построен
                @rtype: C{list}
                """

                defer_list = []

                if type(_type) is Array:
                    placer = placerList(placer([]))
                    
                    for val in value:
                        defer_list.extend(serializeValue(placer, _type.elementType, val))
                elif issubclass(_type, Interface):
                    d = value.serialize()
                    d.addCallback(placer)
                    defer_list.append(d)
                elif _type is datetime:
                    placer(DateTime.toISO(value))
                else:
                    placer(value)

                return defer_list

            result = {}
            defer_list = []

            for (param, value) in self._holder.iteritems():
                defer_list.extend(serializeValue(placerHash(result, param), self._signature[param]['type'], value))

            dl = defer.DeferredList(defer_list, fireOnOneErrback = 1)
            dl.addCallback(lambda _: result)

            return dl

        def getUnserialized(self, serializedParams):
            """Восстанавливаем параметры из сериализованного представления

            @param serializedParams : сериализованные параметры
            """

            def unserializeValue(_type, value):
                """Восстанавливаем переменную из сериализованного значения
                """
                if type(_type) is Array:
                    return [unserializeValue(_type.elementType, val) for val in value]

                if issubclass(_type, Interface):
                    serializer = get_serializer(_type)
                    unservalue = serializer.unserialize(value)
                    return unservalue

                if _type is datetime:
                    return DateTime.fromISO(value)

                if type(value) is types.UnicodeType:
                    return value.encode('utf-8')

                return value

            if isinstance(serializedParams, list) and len(serializedParams) == 0:
                return

            for (param, value) in serializedParams.iteritems():
                if param not in self._signature:
                    raise AttributeError, param

                self.__setattr__(param, unserializeValue(self._signature[param]['type'], value))

        def __prep__(self):
            return "%s VALUES %s" % (object.__prep__(self), self._holder.__prep__())

        def __str__(self):
            return "%s VALUES %s" % (object.__str__(self), self._holder.__str__())

    def __init__(self):
        """
        Конструктор команды
        """
        self._params = {}
        self._result = {}
        self.params = Command._ParamsWrapper(self.commandSignature, self._params)
        self.result = Command._ParamsWrapper(self.resultSignature, self._result)

    def getResponse(self):
        """
        Сформировать результат команды как хэш, готовый к XML-RPC преобразованию.

        @return: Deferred C{dict}, хеш результата команды
        @rtype: L{twisted.internet.defer.Deferred}
        """
        return self.result.getSerialized()

    def getParams(self):
        """
        Сформировать параметры команды как хэш, готовый к XML-RPC преобразованию.

        @return: Deferred C{dict}, хеш параметров команды команды
        @rtype: L{twisted.internet.defer.Deferred}
        """
        return self.params.getSerialized()

    def checkParams(self):
        """
        Проверить наличие всех необходимых параметров команды.

        @raise errors.CommandParamsMissingException: не хватает параметра
        """
        try:
            self.params.checkSignature()
        except AttributeError, (param):
            raise errors.CommandParamsMissingException, param

    def checkResult(self):
        """
        Проверить наличие всех необходимых полей в результате выполнения команды.

        @raise errors.CommandResultMissingException: не хватает значения
        """
        try:
            self.result.checkSignature()
        except AttributeError, (param):
            raise errors.CommandResultMissingException, param

    def init(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.

        Может быть синхронным, а может возвращать L{twisted.internet.defer.Deferred}
        """

    def finalize(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения завершения
        обработки команды.
        """

    def run(self):
        """
        Выполнить команду.

        В процессе выполнения команды или проверки условий её выполнения (наличие всех параметров)
        и т.п., могут возникать исключения, которые будут переданы через errback к deferred, или
        в случае успешного выполнения вызовется callback.

        @return: deferred, которая будет вызвана после завершения выполнения команды
                 и формирования её результата
        @rtype: L{defer.Deferred}
        """
        def checkResult(result):
            self.checkResult()
            return result

        def finalize(res):
            try:
                self.finalize()
            except:
                if not sys.modules.has_key('twisted.trial.runner'):
                    log.err(failure.Failure())

            return res

        try:
            self.checkParams()
            d = defer.maybeDeferred(self.init).addCallback(lambda _: defer.maybeDeferred(self.perform))
        except errors.BaseCommandException:
            return defer.fail()    
        
        return d.addCallback(checkResult).addBoth(finalize)
