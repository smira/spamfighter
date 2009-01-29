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
Подсистема временного хранения данных в памяти.
"""

import sys
from zope.interface import implements

from twisted.internet import reactor, defer

from spamfighter.utils.time import time
from spamfighter.interfaces import IExpirableStorage, IUnreliableStorage, IDomainBindable

class MemoryStorage(object):
    """
    Хранилище пар (ключ, значение) в памяти. Каждая
    пара имеет индивидуальное время жизни. По истечении срока
    жизни пара удаляется из хранилища.

    Удаление ключей из памяти происходит либо при обращении ключу,
    либо по периодически запускаемой задаче, которая уничтожает
    просроченные ключи массово.

    @ivar hash: хэш вида: ключ -> (время_жизни, значение)
    @type hash: C{dict}
    @ivar deleteQueue: "очередь" ключей на удаление, хэш вида: 
       момент_удаления -> { хэш ключ_на_удаление -> 1 }
    @type deleteQueue: C{dict}
    @ivar deleteInterval: интервал группировки ключей на удаление в секундах (ключи с
       временем жизни в данном интервале будут удалены общей пачкой)
    @type deleteInterval: C{int}
    @ivar cleanupInterval: интервал запуска задачи очистки просроченных ключей
    @type cleanupInterval: C{int}
    @ivar lastDeleteTime: первый момент удаления ключей для следующего запуска задачи
        очистки
    @type lastDeleteTime: C{int}

    @cvar instance: синглтон-экземпляр MemoryStorage
    @type instance: L{MemoryStorage}
    """
    implements(IExpirableStorage, IUnreliableStorage)

    instance = None

    def __init__(self, deleteInterval=10, cleanupInterval=60):
        """
        Конструктор.

        @param deleteInterval: интервал группировки ключей на удаление в секундах (ключи с
           временем жизни в данном интервале будут удалены общей пачкой)
        @type deleteInterval: C{int}
        @param cleanupInterval: интервал запуска задачи очистки просроченных ключей, если
           интервал 0, то задача очистки не запускается никогда
        @type cleanupInterval: C{int}
        """
        self.hash = dict()
        self.deleteQueue = dict()
        self.deleteInterval = deleteInterval
        self.cleanupInterval = cleanupInterval
        self.lastDeleteTime = time() / self.deleteInterval
        self.cleanupDelayed = None

        if self.cleanupInterval != 0:
            self.cleanupDelayed = reactor.callLater(self.cleanupInterval, self._cleanup)

    def _cleanup(self):
        """
        Очистить старые ключи. 

        Метод либо вызывается автоматически через каждые L{cleanupInterval} секунд,
        либо может вызываться в любой момент времени.
        """
        self.cleanupDelayed = None

        curDeleteTime = time() / self.deleteInterval
        todoIntervals = xrange(self.lastDeleteTime, curDeleteTime)

        for interval in todoIntervals:
            todo = self.deleteQueue.get(interval, {})
            for key in todo.iterkeys():
                del self.hash[key]
            if interval in self.deleteQueue:
                del self.deleteQueue[interval]

        self.lastDeleteTime = curDeleteTime
        if self.cleanupInterval != 0:
            self.cleanupDelayed = reactor.callLater(self.cleanupInterval, self._cleanup)

    def _exists(self, key):
        """
        Внутренний метод: существует ли указанный ключ в хранилище?

        @rtype: C{bool}
        """
        if not self.hash.has_key(key):
            return False

        data = self.hash[key]
        if data[0] != 0 and data[0] <= time():
            del self.hash[key]
            del self.deleteQueue[data[0] / self.deleteInterval][key]
            return False

        return True

    def set(self, key, value, expire):
        """
        Записать (перезаписать) значение ключа.

        @param key: ключ
        @type key: C{str}
        @param value: значение
        @type value: C{str} или C{int}
        @param expire: время жизни ключа в секундах, 0 - хранить "вечно"
        @type expire: C{int}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """
        if expire != 0:
            expire = time() + expire
        if self.hash.has_key(key):
            data = self.hash[key]
            if data[0] != 0:
                del self.deleteQueue[data[0] / self.deleteInterval][key]

        self.hash[key] = (expire, value)
        if expire != 0:
            if not self.deleteQueue.has_key(expire / self.deleteInterval):
                self.deleteQueue[expire / self.deleteInterval] = dict()
            self.deleteQueue[expire / self.deleteInterval][key] = 1

        return defer.succeed(None)

    def get(self, key):
        """
        Получить значения ключа.

        Если ключ не найден (не существует, потерян, истекло время жизни), 
        возвращается исключение C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @return: Deferred значение ключа, C{str} или C{int}
        @rtype: C{twisted.internet.Deferred}
        """
        if not self._exists(key):
            return defer.fail(KeyError(key))

        return defer.succeed(self.hash[key][1])

    def add(self, key, value, expire):
        """
        Добавить ключ в хранилище.

        Операция аналогична C{set}, но если ключ уже существует,
        будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: значение
        @param expire: время жизни ключа в секундах, 0 - хранить "вечно"
        @type expire: C{int}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """
        if self._exists(key):
            return defer.fail(KeyError(key))

        return self.set(key, value, expire)

    def append(self, key, value):
        """
        Дописать в конец значения ключа еще один элемент.
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: дописываемое значение
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """
        if not self._exists(key):
            return defer.fail(KeyError(key))

        if not isinstance(value, str):
            return defer.fail(TypeError(value))

        if not isinstance(self.hash[key][1], str):
            return defer.fail(TypeError(self.hash[key][1]))

        self.hash[key] = (self.hash[key][0], self.hash[key][1] + value)
        return defer.succeed(None)

    def delete(self, key):
        """
        Удалить ключ из хранилища. 

        Если ключ не найден, возвращается исключение C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """
        if not self._exists(key):
            return defer.fail(KeyError(key))
    
        if self.hash[key][0] != 0:
            del self.deleteQueue[self.hash[key][0] / self.deleteInterval][key]
        del self.hash[key]
        return defer.succeed(None)

    def incr(self, key, value=1):
        """
        Увеличить значени счетчика на указанное значение
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: значение на которое увеличиваем
        @type value: C{int}
        @return: Deferred о завершении операции, C{int}
        @rtype: C{twisted.internet.Deferred}
        """
        if not self._exists(key):
            return defer.fail(KeyError(key))

        if not isinstance(value, int):
            return defer.fail(TypeError(value))

        if not isinstance(self.hash[key][1], int):
            return defer.fail(TypeError(self.hash[key][1]))

        self.hash[key] = (self.hash[key][0], self.hash[key][1] + value)
        return defer.succeed(self.hash[key][1])

    @staticmethod
    def getInstance():
        """
        Получить синглтон-экземпляр хранилища.

        @rtype: L{MemoryStorage}
        """
        if MemoryStorage.instance is None:
            if not sys.modules.has_key('twisted.trial.runner'):
                MemoryStorage.instance = MemoryStorage()
            else:
                MemoryStorage.instance = MemoryStorage(cleanupInterval=0)

        return MemoryStorage.instance
        
class DomainMemoryStorage(object):
    """
    Хранилище в памяти, которое располагается в домене.

    Все хранилища в доменах разделяют один общий экземпляр L{MemoryStorage}, 
    префиксируя доступ к ключам ключом домена.
    """
    implements(IExpirableStorage, IUnreliableStorage, IDomainBindable)

    def __init__(self, storage=None):
        self.prefix = None
        if storage is None:
            self.storage = MemoryStorage.getInstance()
        else:
            self.storage = storage

    def bind(self, domain, name):
        """
        Извещение объекту о том, что он был помещен в домен.

        @param domain: домен
        @type domain: L{IDomain}
        @param name: имя в домене
        @type name: C{str}
        """
        self.prefix = domain.key() + '_' + name

    def set(self, key, value, expire):
        return self.storage.set(self.prefix + key, value, expire)

    def get(self, key):
        return self.storage.get(self.prefix + key)

    def add(self, key, value, expire):
        return self.storage.add(self.prefix + key, value, expire)

    def append(self, key, value):
        return self.storage.append(self.prefix + key, value)

    def incr(self, key, value=1):
        return self.storage.incr(self.prefix + key, value)

    def delete(self, key):
        return self.storage.delete(self.prefix + key)

    def __getstate__(self):
        if self.storage is not MemoryStorage.getInstance():
            raise TypeError, "not bound to default storage"
        return 1

    def __setstate__(self, state):
        self.__init__()
