# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Модель анализа сообщений по Байесу.
"""

from zope.interface import implements
from twisted.internet import defer

from spamfighter.interfaces import IModel
from spamfighter.core.model.thomas import Bayes

class BayesModel(object):
    """
    Модель анализа сообщений по Байесу.

    @ivar bayes: анализатор по Байесу
    @type bayes: L{Bayes}
    """
    implements(IModel)

    def __init__(self):
        """
        Конструктор.
        """
        self.bayes = Bayes()

    def train(self, text, good):
        """
        Обучить модель на указанном тексте.

        @param text: текст, на котором обучаемся
        @type text: C{unicode}
        @param good: хороший это текст или плохой с точки зрения классификации?
        @type good: C{bool}
        @return: результат операции
        @rtype: C{Deferred}
        """
        if good:
            pool = 'good'
        else:
            pool = 'bad'
        self.bayes.train(pool, text)
        return defer.succeed(True)

    def classify(self, text):
        """
        Классифицировать текст согласно модели.

        Результат классификации - текст "хороший" или "плохой" (относительно модели).

        @param text: текст, который классифируем
        @type text: C{unicode}
        @return: результат операции, C{bool}, хороший ли текст?
        @rtype: C{Deferred}
        """
        result = self.bayes.guess(text)
        if len(result) == 0:
            return defer.succeed(True)
        if 'bad' == result[0][0]:
            return defer.succeed(False)
        return defer.succeed(True)

