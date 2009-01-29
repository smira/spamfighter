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
Правила, управляющие логом сообщений.
"""

from spamfighter.core.rules import factory
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.commands import errors
from spamfighter.interfaces import IMessageLog

def messageLogPut(domain, message, log='messageLog', tag=None):
    """
    Поместить сообщение в лог сообщений.

    Дополнительно можно при помещении в лог указать дополнительный тэг, который будет сохранен в логе
    вместе с сообщением.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param log: имя свойства домена, содержащего лог сообщений
    @type log: C{str}
    @param tag: дополнительный тэг, записываемый в лог
    @type tag: C{str}
    """
    try:
        messageLog = domain.get(log)
    except DomainKeyError:
        raise errors.AttributeKeyException, log

    if not IMessageLog.providedBy(messageLog):
        raise errors.NotAMessageLogError, log
    
    if tag is None:
        tags=[]
    else:
        tags=[tag]

    return messageLog.put(message=message, tags=tags).addCallback(lambda _: True)

factory.registerRule(messageLogPut)
