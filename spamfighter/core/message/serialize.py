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
Сериализация сообщений, взаимодействие с командами.
"""

from zope.interface import implements
from twisted.internet import defer

from spamfighter.interfaces import IMessage
from spamfighter.core.commands.serialize import ISerializable, register_serializer
from spamfighter.core.commands import errors
from spamfighter.core.message.message import Message

class ITransitMessage(ISerializable):
    """
    Вариант сообщения, которое передается в сериализованном представлении
    через параметры команд.
    """

    def getMessage(domain):
        """
        Окончательно десериализовать сообщение относительно домена.

        @param domain: домен, относительно которого десериализуется сообщение
        @type domain: L{spamfighter.interfaces.IDomain}
        """

class TransitMessage(object):
    """
    Вариант сообщения, которое передается в сериализованном представлении
    через параметры команд.

    @ivar serialized: сериализованное представление сообщения
    @type serialized: C{dict}
    """

    implements(ITransitMessage)
    register_serializer(ITransitMessage)

    def __init__(self, message=None, serialized=None):
        """
        Конструктор.

        Может быть передано либо сериализованное представление сообщения (C{serialized}), либо
        исходное сообщение (C{message}).

        @param message: исходное сообщение
        @type message: L{IMessage}
        @param serialized: сериализованное представление сообщения
        @type serialized: C{dict}
        """

        if serialized is not None:
            assert message is None
            self.serialized = serialized
        else:
            assert serialized is None
            assert IMessage.providedBy(message)
            
            self.serialized = {}
            for attribute in message:
                self.serialized[attribute.domain().name()] = attribute.serialize()

    def serialize(self):
        """
        Сериализовать сообщение.
        """
        return defer.succeed(self.serialized)

    @classmethod
    def unserialize(cls, serialized):
        """
        Десериализовать сообщение.

        @param serialized: сериализованное представление сообщения
        @type serialized: C{dict}
        """
        return TransitMessage(serialized=serialized)

    def getMessage(self, domain):
        """
        Окончательно десериализовать сообщение относительно домена.

        @param domain: домен, относительно которого десериализуется сообщение
        @type domain: L{spamfighter.interfaces.IDomain}
        @return: десериализованное сообщение
        @rtype: L{IMessage}
        """
        messageDomain = domain.get('messageDomain')
        
        try:
            return Message([messageDomain[name].deserialize(value) for name, value in self.serialized.iteritems()])
        except KeyError, name:
            raise errors.AttributeKeyException(name)

    def __repr__(self):
        return "TransitMessage(serialized=%r)" % self.serialized

    def __eq__(self, other):
        if not isinstance(other, TransitMessage):
            return False
            
        return self.serialized == other.serialized
