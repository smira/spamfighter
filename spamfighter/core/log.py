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
Лог сообщений, прошедших через firewall.
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from twisted.internet import defer
from zope.interface import implements, Interface, Attribute

from spamfighter.core.message import TransitMessage
from spamfighter.core.message.serialize import ISerializable, register_serializer
from spamfighter.interfaces import IDomainBindable, IMessageLog, ITaggedMessage, IMessage, ILogEntry
from spamfighter.utils.time import time

class LogEntry(object):
    """
    Объект отдельной записи в логе.

    Объект должен быть сериализуемым (для передачи в рамках API), а также
    pickle'уемым (для хранения в storage).

    @ivar when: время и дата сообщения, UTC
    @type when: C{int}
    @ivar message: само сообщение
    @type message: L{TransitMessage}
    @ivar tags: тэги, привязанные к сообщению
    @type tags: C{list(str)}
    @ivar id: ID записи
    @type id: C{int}
    """
    implements(ILogEntry, ISerializable)
    register_serializer(ILogEntry)

    def __init__(self, when, message, tags=None, id=None):
        """
        Конструктор.

        @param when: дата/время записи в логе, UTC
        @type when: C{int}
        @param message: само сообщение
        @type message: L{IMessage} или L{ITaggedMessage} или L{TransitMessage}
        @param tags: тэги, привзяанные к сообщению
        @type tags: C{list(str)}
        """
        if when is None:
            when = time()
        self.when = when
        if tags is None:
            tags = []
        self.tags = tags
        if IMessage.providedBy(message):
            if ITaggedMessage.providedBy(message):
                self.tags.extend(message.getTags())
            message = TransitMessage(message=message)
        self.message = message
        self.id = id
        
    def serialize(self):
        """
        Сериализовать запись в логе.
        """
        return self.message.serialize().addCallback(lambda message : { 'when' : self.when, 'message' : message, 'tags' : self.tags, 'id' : self.id });

    @classmethod
    def unserialize(cls, serialized):
        """
        Десериализовать сообщение.

        @param serialized: сериализованное представление сообщения
        @type serialized: C{dict}
        """
        return LogEntry(when=serialized['when'], message=TransitMessage(serialized=serialized['message']), tags=serialized['tags'], id=serialized['id'])

    def __repr__(self):
        return 'LogEntry(when=%r, tags=%r, message=%r, id=%r)' % (self.when, self.tags, self.message, self.id)

    def __eq__(self, other):
        if not isinstance(other, LogEntry):
            return False

        return self.when == other.when and self.tags == other.tags and self.message == other.message and self.id == other.id

class MessageLog(object):
    """
    Лог сообщений, проходящих через сервер.

    Класс поддерживает эффективный, потенциально распределенный кольцевой лог заданного масштаба.
    Элементы лога (C{LogEntry}) хранятся в pickled-представлении в storage. В одном ключе хранятся
    все сообщения, попавшие в лог в течение C{timeChunk} секунд, при этом поддерживается C{numChunks}
    ключей всего. Общая минимальная емкость лога составляет C{timeChunk}*(C{numChunks}-1) секунд.

    @ivar storageName: имя свойства в домене, которое является хранилищем лога
    @type storageName: C{str}
    @ivar storage: хранилище
    @type storage: L{spamfighter.interfaces.IExpirableStorage}
    @ivar timeChunk: емкость одного ключа в хранилище в секундах
    @type timeChunk: C{int}
    @ivar numChunks: число выделяемых в хранилище ключей под лог
    @type numChunks: C{int}
    @ivar keyTemplate: шаблон имени ключа хранилища под лог
    @type keyTemplate: C{str}
    @ivar lastID: последний выделенный ID для записи лога
    @type lastID: C{int}
    """
    implements(IDomainBindable, IMessageLog)

    def __init__(self, storage='storage', timeChunk=10, numChunks=100):
        """
        Конструктор.

        @param storage: имя свойства в домене, которое является хранилищем лога
        @type storage: C{str}
        @param timeChunk: емкость одного ключа в хранилище в секундах
        @type timeChunk: C{int}
        @param numChunks: число выделяемых в хранилище ключей под лог
        @type numChunks: C{int}
        """
        self.storageName = storage
        self.timeChunk = timeChunk
        self.numChunks = numChunks
        self.lastID = 1

    def bind(self, domain, name):
        """
        Извещение объекту о том, что он был помещен в домен.

        @param domain: домен
        @type domain: L{IDomain}
        @param name: имя в домене
        @type name: C{str}
        """
        self.storage = domain.get(self.storageName)
        self.keyTemplate = 'ml' + name + '_%d';

    def put(self, message, when=None, tags=None):
        """
        Поместить новое сообщение в лог.

        @param when: дата/время записи в логе, UTC
        @type when: C{int}
        @param message: само сообщение
        @type message: L{IMessage} или L{ITaggedMessage} или L{TransitMessage}
        @param tags: тэги, привзяанные к сообщению
        @type tags: C{list(str)}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.defer.Deferred}
        """
        data = LogEntry(when=when, message=message, tags=tags, id=self.lastID)
        self.lastID = self.lastID + 1

        serialized = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

        key = self.keyTemplate % (data.when / self.timeChunk % self.numChunks)

        def keyExists(failure):
            failure.trap(KeyError)

            return self.storage.append(key, serialized).addErrback(noSuchKey)

        def noSuchKey(failure):
            failure.trap(KeyError)

            return self.storage.add(key, serialized, self.timeChunk * (self.numChunks-1)).addErrback(keyExists)

        return self.storage.append(key, serialized).addErrback(noSuchKey)

    def fetch(self, first=None, last=None, firstID=None):
        """
        Произвести выборку сообщений из лога по указанным критериям выборки.

        @param first: минимальная дата возвращаемого сообщения
        @type first: C{int}
        @param last: максимальная дата возвращаемого сообщения
        @type last: C{int}
        @param firstID: минимальный ID элемента лога, который будет возвращен
        @type firstID: C{int}
        @return: Deferred с C{list(}L{ILogEntry}C{)}
        @rtype: C{twisted.internet.defer.Deferred} 
        """
        if last is None or last > time():
            last = time()

        if first is None or last < first or (last-first) > self.timeChunk * (self.numChunks-1):
            first = time() - self.timeChunk * (self.numChunks-1)

        firstKey = first / self.timeChunk % self.numChunks
        lastKey = last / self.timeChunk % self.numChunks

        if firstKey < lastKey:
            keyRange = range(firstKey, lastKey+1)
        else:
            keyRange = range(firstKey, self.numChunks) + range(0, lastKey+1)

        def logFetched(data):
            result = []

            for item in data:
                if item[0] == defer.FAILURE:
                    continue

                input = StringIO.StringIO(item[1])

                while True:
                    try:
                        data = pickle.load(input)
                        if data.when >= first and data.when <= last:
                            if firstID is None or data.id >= firstID:
                                result.append(data)
                    except EOFError:
                        break

            return result

        return defer.DeferredList([self.storage.get(self.keyTemplate % key) for key in keyRange], consumeErrors=1).addCallback(logFetched)

    def __getstate__(self):
        return { 'storage' : self.storageName, 'numChunks' : self.numChunks, 'timeChunk' : self.timeChunk }

    def __setstate__(self, state):
        self.__init__(**state)
