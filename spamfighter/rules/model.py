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
Правила, управляющие моделями.
"""

from spamfighter.interfaces import IModel
from spamfighter.core.commands import errors
from spamfighter.core.rules import factory
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.message import AttributeNotFoundError

class ModelRule(object):
    """
    Базовый класс для правило, использующее модель анализа сообщений.

    @ivar model: модель анализа сообщений
    @type model: L{IModel}
    @ivar modelName: имя модели в домене
    @type modelName: C{str}
    @ivar text: текст сообщения
    @type text: C{unicode}
    """
    def __init__(self, model="model"):
        """
        Конструктор.

        @param model: имя модели в домене
        @type model: C{str}
        """
        self.modelName = model

    def analyze(self, domain, message, attribute="text"):
        """
        Анализ сообщения.

        @param domain: домен, относительно которого идёт анализ
        @type domain: L{IDomain}
        @param message: сообщение
        @type message: L{spamfighter.interfaces.IMessage}
        @param attribute: имя атрибута сообщения, содержащего текст
        @type attribute: C{str}
        """
        try:
            self.model = domain.get(self.modelName)
        except DomainKeyError:
            raise errors.AttributeKeyException, self.modelName

        if not IModel.providedBy(self.model):
            raise errors.NotAModelError, self.modelName

        try:
            self.text = message[attribute].value()
        except AttributeNotFoundError:
            raise errors.MessageAttributeKeyException, attribute

class modelClassify(ModelRule):
    """
    Классификация сообщения по модели: истинно, если модель сообщает, что сообщение
    относится к классу *плохих*.
    """
    def analyze(self, domain, message, **kwargs):
        super(modelClassify, self).analyze(domain, message, **kwargs)

        return self.model.classify(self.text)

class modelTrain(ModelRule):
    """
    Обучить модель на сообщении: всегда истинно.
    """
    def analyze(self, domain, message, marker="good", **kwargs):
        """
        @param marker: тип сообщения для модели, "good" или "bad"
        @type marker: C{str}
        """
        super(modelTrain, self).analyze(domain, message, **kwargs)

        return self.model.train(self.text, marker == "good").addCallback(lambda _: True)

factory.registerRule(modelClassify)
factory.registerRule(modelTrain)
