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

