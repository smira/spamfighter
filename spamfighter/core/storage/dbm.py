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
Подсистема хранения данных на локальном диске в BDB-подобной БД.
"""

import anydbm
import os.path
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

from zope.interface import implements
from twisted.internet import defer

from spamfighter.interfaces import IPersistentStorage, IExpirableStorage, IDomainBindable
from spamfighter.utils.time import time
from spamfighter.utils import config

class DBMStorage(object):
    """
    Надежное хранилище ключей. Элементы хранилища хранятся в BDB (C{anydbm}) базе данных
    на локальном диске. Поддерживается интерфейс expire-ключей (удаляемых по истечение некоторого
    времени).

    @ivar db: ссылка на базу данных C{anydbm}
    """
    implements(IPersistentStorage, IExpirableStorage)

    def __init__(self, dir, name):
        """
        Конструктор.

        @param dir: подкаталог, в котором должны храниться файлы БД
        @type dir: C{str}
        @param name: имя БД
        @type name: C{str}
        """
        dir = os.path.join(config.storage.dbm.path, dir)
        if not os.path.exists(dir):
            os.mkdir(dir)

        self.db = anydbm.open(os.path.join(dir, name + '.db'), 'c')

    def _fetch(self, key):
        """
        Получить значение ключа.

        @param key: ключ
        @type key: C{str}
        @return: пара (срок_годности, значение), если ключ есть в БД или (None, None), если он отсутствует
        """
        if not self.db.has_key(key):
            return (None, None)

        (expire, value) = pickle.loads(self.db[key])

        if expire != 0 and expire <= time():
            del self.db[key]
            return (None, None)

        return (expire, value)

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
            expire += time()
        
        self.db[key] = pickle.dumps((expire, value), pickle.HIGHEST_PROTOCOL)
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
        (expire, value) = self._fetch(key)

        if value is None:
            return defer.fail(KeyError(key))

        return defer.succeed(value)

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
        dummy, val = self._fetch(key)

        if val is not None:
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
        expire, old = self._fetch(key)

        if old is None:
            return defer.fail(KeyError(key))
        
        if not isinstance(value, str):
            return defer.fail(TypeError(value))

        if not isinstance(old, str):
            return defer.fail(TypeError(old))

        value = old + value
        self.db[key] = pickle.dumps((expire, value), pickle.HIGHEST_PROTOCOL)
        return defer.succeed(None)

    def incr(self, key, value=1):
        """
        Увеличить значение ключа на единицу (тип значения - целое число).
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: величина инкремента
        @type value: C{int}
        @return: Deferred с новым значением ключа, C{int}
        @rtype: C{twisted.internet.Deferred}
        """
        expire, old = self._fetch(key)

        if old is None:
            return defer.fail(KeyError(key))
        
        if not isinstance(value, int):
            return defer.fail(TypeError(value))

        if not isinstance(old, int):
            return defer.fail(TypeError(old))

        value = old + value
        self.db[key] = pickle.dumps((expire, value), pickle.HIGHEST_PROTOCOL)
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
        expire, value = self._fetch(key)

        if value is None:
            return defer.fail(KeyError(key))

        del self.db[key]
        return defer.succeed(None)

class DomainedDBMStorage(object):
    """
    Надежное хранилище ключей. Вариант с привязкой к домену.

    @ivar db: ссылка на базу данных C{anydbm}
    """
    implements(IPersistentStorage, IExpirableStorage, IDomainBindable)

    def __init__(self):
        """
        Конструктор.
        """
        self.db = None

    def bind(self, domain, name):
        """
        Извещение объекту о том, что он был помещен в домен.

        @param domain: домен
        @type domain: L{IDomain}
        @param name: имя в домене
        @type name: C{str}
        """
        assert self.db is None
        self.db = DBMStorage(domain.key(), name)

    def _check_db(self):
        """
        Проверить, что база данных уже открыта (доступна).
        """
        assert self.db is not None

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
        return self.db.set(key, value, expire)

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
        return self.db.get(key)

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
        return self.db.add(key, value, expire)

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
        return self.db.append(key, value)

    def incr(self, key, value=1):
        """
        Увеличить значение ключа на единицу (тип значения - целое число).
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: величина инкремента
        @type value: C{int}
        @return: Deferred с новым значением ключа, C{int}
        @rtype: C{twisted.internet.Deferred}
        """
        return self.db.incr(key, value)

    def delete(self, key):
        """
        Удалить ключ из хранилища. 

        Если ключ не найден, возвращается исключение C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """
        return self.db.delete(key)

    def __getstate__(self):
        return 1

    def __setstate__(self, state):
        self.__init__()
