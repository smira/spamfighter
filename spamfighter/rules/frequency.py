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
Набор правил проверки текста сообщений на частоту
"""

import hashlib
import re

from spamfighter.core.rules import factory

def calculateMD5(string):
    """
    Вычисление md5 от строки в любой кодировки.

    @param string: строка для которой надо посчитать md5
    @type string: C{unicode}
    @return: значение md5
    @rtype: C{str}
    """

    return hashlib.md5(string.encode('utf-8', 'strict')).hexdigest()

clearMessageRE = re.compile(u'[^\w]', re.U)

def clearMessage(text):
    """
    Функция удаления из текста сообщения всех символов, кроме букв.

    @param text: текст сообщения, который мы будем анализировать
    @type text: C{unicode}
    @return: значение md5
    @rtype: C{unicode}
    """

    return clearMessageRE.sub('', text).lower()

def messageFrequencyCheck(domain, message, attribute='text', storage='storage', timeout=300, count=3, minLength=10):
    """
    Правило проверки сообщение на частоту повторения.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения, содержащего поле для проверки
    @type attribute: C{str}
    @param storage: имя атрибута домена, содержащего хранилище
    @type storage: C{str}
    @param timeout: время не повторения сообщения, секунды
    @type timeout: C{int}
    @param count: максимально допустимое количество сообщение в указанный период времени
    @type count: C{int}
    @param minLength: минимальная длина сообщения для анализа
    @type minLength: C{int}
    """

    text = message.get(attribute).value()
    if len(text) < minLength:
        return True

    storage = domain.get(storage)
    message_key = 'mfreq_' + attribute + calculateMD5( clearMessage(message.get(attribute).value()) )

    def gotKey(value):
        if value < count:
            return storage.incr(message_key).addCallback(lambda value: value < count).addErrback(noKey)
        else:
            return False

    def noKey(failure):
        failure.trap(KeyError)

        def errback(failure):
            failure.trap(KeyError)
            return gotKey(0)

        return storage.add(message_key, 1, timeout).addCallback(lambda _: True).addErrback(errback)

    return storage.get(message_key).addCallbacks(gotKey, noKey)

def userFrequencyCheck(domain, message, attribute='from', storage='storage', timeout=300, count=3):
    """
    Правило проверки сообщения на частоту отправки указанным пользователем.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения, содержащее идентификатор пользователя отославшего его
    @type attribute: C{int}
    @param storage: имя атрибута домена, содержащего хранилище
    @type storage: C{str}
    @param timeout: время в течении которого пользователь может отправлять указанное количество сообщений
    @type timeout: C{int}
    @param count: максимально допустимое количество сообщение в указанный период времени
    @type count: C{int}
    """
    storage = domain.get(storage)
    user_key = 'ufreq_' + attribute + str(message.get(attribute).serialize())

    def gotKey(value):
        if value < count:
            return storage.incr(user_key).addCallback(lambda value: value < count).addErrback(noKey)
        else:
            return False

    def noKey(failure):
        failure.trap(KeyError)

        def errback(failure):
            failure.trap(KeyError)
            return gotKey(0)

        return storage.add(user_key, 1, timeout).addCallback(lambda _: True).addErrback(errback)

    return storage.get(user_key).addCallbacks(gotKey, noKey)

factory.registerRule(userFrequencyCheck)
factory.registerRule(messageFrequencyCheck)
