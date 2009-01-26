# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Набор правил аналица текста сообщений
"""

import re

from itertools import imap
from spamfighter.core.rules import factory

clearSpacesRE = re.compile(u'[\s]', re.U)

def messageFloodCheck(domain, message, attribute='text', minLength=16, minMean=1.5, maxVariance=2.0):
    """
    Правило проверки сообщения на наличие флуда.
    Наличие флуда в фразе определяется частотой повторения триграмм. При запуске на тестовой базе, содержащей нормальные сообщения,
    из 16674 сообщений функция не заблокировала ни одного сообщения. При запуске на тестовой базе, содержащей флуд, из 1477 было обнаружено
    956 сообщений, что составляет 65% от общего числа сообщений.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения, содержащего текст
    @type attribute: C{str}
    @param minLength: минимальная длина сообщения для анализа
    @type minLength: C{int}
    @param minMean: минимальное значение математического ожидания
    @type minMean: C{float}
    @param maxVariance: максимальное значение дисперсии
    @type maxVariance: C{float}
    """

    str = clearSpacesRE.sub('', message.get(attribute).value()).lower()

    if len(str) < minLength:
        return True

    result = {}
    for i in xrange(len(str)-2):
        result[str[i:i+3]] = result.get(str[i:i+3], 0) + 1

    s = sum(result.itervalues())
    sum_sqr = sum(imap(lambda x: x*x, result.itervalues()))
    n = len(result)

    mean = s/float(n) if n > 0 else 0
    variance = (sum_sqr - s*mean)/float(n-1) if n > 1 else 0

    if mean > minMean and variance < maxVariance:
        return False

    return True

factory.registerRule(messageFloodCheck)
