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
Модуль содержащий правила проверки сообщений
"""

import re

from spamfighter.core.rules import factory
from spamfighter.core.message.attribute import AttributeNotFoundError

class regexpCheck(object):
    """
    Правило проверки текст сообщение на соответствие регулярному выражению.

    @ivar compiledRe: скомпилированное регулярное выражение
    @type compiledRe: C{re}
    """
    def __init__(self, regexp):
        """
        Конструктор.

        @param regexp: регулярное выражение для анализа
        @type regexp: C{unicode}
        """
        self.compiledRe = re.compile(regexp, re.U)

    def analyze(self, domain, message, attribute='text'):
        """
        Функция анализа сообщения на соответствие регулярному выражению

        @param domain: домен, относительно которого идёт анализ
        @type domain: L{IDomain}
        @param message: сообщение
        @type message: L{spamfighter.interfaces.IMessage}
        @param attribute: имя атрибута сообщения, содержащего текст
        @type attribute: C{str}
        """

        return self.compiledRe.match(message.get(attribute).value()) is not None

def lengthCheck(domain, message, minLength=None, maxLength=None, attribute='text'):
    """
    Правило проверки текста сообщение на минимальную и максимальную длину.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения, содержащего текст
    @type attribute: C{str}
    @param minLength: минимальная длина сообщения
    @type minLength: C{int}
    @param minLength: максимальная длина сообщения
    @type minLength: C{int}
    """

    if minLength is not None and len(message.get(attribute).value()) < minLength:
        return False

    if maxLength is not None and len(message.get(attribute).value()) > maxLength:
        return False

    return True

def attributeCheck(domain, message, attribute, value):
    """
    Правило проверки соответствия значения атрибута указанному значению.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения для проверки на соответствие
    @type attribute: C{str}
    @param value: значение для проверки на соответствие
    @type value: C{object}
    """

    return message.get(attribute).value() == value

def hasAttribute(domain, message, attribute):
    """
    Правило проверки наличия аттрибута у сообщения

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения для проверки на наличие
    @type attribute: C{str}
    """

    try:
        message.get(attribute)
        return True
    except AttributeNotFoundError:
        return False

factory.registerRule(regexpCheck)
factory.registerRule(lengthCheck)
factory.registerRule(hasAttribute)
factory.registerRule(attributeCheck)
