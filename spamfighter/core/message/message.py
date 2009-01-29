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
Сообщения, домены сообщений.
"""

from zope.interface import implements

from spamfighter.core.message.attribute import AttributeNotFoundError
from spamfighter.interfaces import IMessageDomain, IMessage, ITaggedMessage

class MessageDomain(object):
    """
    Список доменов атрибутов, которые должны быть у сообщения.

    Такой объект хранится в домене.

    @param attrs: список доменов атрибутов (типов атрибутов)
    @type attrs: C{dict}
    """
    implements(IMessageDomain)

    def __init__(self, *args):
        """
        Конструктор.

        @param *args: список доменов атрибутов, каждый L{IAttributeDomain}
        @type *args: C{list}
        """
        self.attrs = {}
        for attr in args:
            self.attrs[attr.name()] = attr

    def names(self):
        """
        Получить список имен доменов атрибутов.

        @return: список имен
        @rtype: C{list(str)}
        """
        return self.attrs.keys()

    def __getitem__(self, key):
        """
        Получить домен атрибута по имени.

        @param key: имя атрибута
        @type key: C{str}
        @return: атрибут домена
        @rtype: L{IAttributeDomain}
        """
        return self.attrs[key]

class Message(object):
    """
    Сообщение - основная единица обработки для Спамоборца.

    Сообщение обладает тремя основными свойствами:
     - от кого;
     - кому;
     - текст;
     - время отправки. 

    Структурно поля "от кого" и "кому" ничем не отличаются, они описывают
    адресанта и адресата сообщения, соответственно. Поле "кому" может
    отсутствовать (например, если это сообщение - девиз пользователя на своей
    странице). Поля "от кого" и "кому" состоят из атрибутов (L{IAttribute}).

    @ivar _attributes: хэш (по имени) атрибутов сообщения
    @type _attributes: C{dict}
    """
    implements(IMessage)

    def __init__(self, attributes):
        """
        Конструктор.

        @param attributes: атрибуты сообщения
        @type attributes: C{list(}L{IAttribute}C{)}
        """
        self._attributes = {}
        for attribute in attributes:
            self._putAttr(attribute)

    def _putAttr(self, attribute):
        """
        Добавить атрибут к сообщению.

        @param attribute: атрибут
        """
        self._attributes[attribute.domain().name()] = attribute

    def get(self, name):
        """
        Получить атрибут по имени.

        @param name: имя атрибута
        @type name: C{str}
        @return: атрибут
        @rtype: L{IAttribute}
        """
        try:
            return self._attributes[name]
        except KeyError:
            raise AttributeNotFoundError, name

    def __getitem__(self, name):
        return self.get(name)

    def __iter__(self):
        return self._attributes.itervalues()

    def __eq__(self, other):
        return isinstance(other, Message) and self._attributes == other._attributes

    def __repr__(self):
        return "Message(%r)" % self._attributes.values()

class TaggedMessage(Message):
    """
    Сообщение с прицепленными к нему тэгами.

    @ivar _tags: список тегов, прицепленных к сообщению
    @type _tags: C{dict}
    """
    implements(ITaggedMessage)

    def __init__(self, *args, **kwargs):
        """
        Конструктор.

        Для создания L{TaggedMessage} из L{Message} необходимо передать
        L{Message} в параметре с именем C{message}.
        """
        if kwargs.has_key('message'):
            message = kwargs['message']
            if isinstance(message, Message):
                kwargs['attributes'] = message._attributes.values()
                del kwargs['message']
        super(TaggedMessage, self).__init__(*args, **kwargs)
        self._tags = {}

    def addTag(self, tag):
        """
        Добавить тэг tag к сообщению.

        @param tag: тэг
        @type tag: C{str}
        """
        self._tags[tag] = 1

    def getTags(self):
        """
        Получить все текущие тэги сообщения.

        @return: список тэгов
        @rtype: C{list(str)}
        """
        return self._tags.keys()

    def checkHasAllTags(self, tags):
        """
        Проверить, содержит ли сообщение все указанные тэги.

        @param tags: список тэгов
        @type tags: C{list(str)}
        @return: содержит ли все указанные тэги?
        @rtype: C{bool}
        """
        for tag in tags:
            if not self._tags.has_key(tag):
                return False

        return True

    def checkHasNoTags(self, tags):
        """
        Проверить, что в сообщении нет ни одного из указанных тэгов.

        @param tags: список тэгов
        @type tags: C{list(str)}
        @return: не содержит ли все указанные тэги?
        @rtype: C{bool}
        """
        for tag in tags:
            if self._tags.has_key(tag):
                return False

        return True

    def __eq__(self, other):
        return isinstance(other, TaggedMessage) and Message.__eq__(self, other) and self._tags == other._tags

    def __repr__(self):
        return "TaggedMessage(%r, tags=%r)" % (self._attributes.values(), self._tags.keys())
