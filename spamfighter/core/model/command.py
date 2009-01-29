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
Базовый класс команд работы с моделью.
"""

import types
from zope.interface import providedBy
from twisted.internet import defer

from spamfighter.interfaces import IModel
from spamfighter.core.commands import DomainedCommand, errors
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.message import ITransitMessage, AttributeNotFoundError

class ModelBaseCommand(DomainedCommand):
    """
    Базовый класс команд, упраявляющих моделью.

    @ivar model: модель, которой мы управляем
    @type model: L{IModel}
    @ivar message: сообщение, на котором мы тренируемся
    @type message: L{IMessage}
    @ivar text: извлеченный текст сообщения
    @type text: C{unicode}
    """

    commandSignature = {
            'model' :           { 'type' : types.StringType, 'required' : True },
            'message' :         { 'type' : ITransitMessage, 'required' : True, },
            'text_attribute' :  { 'type' : types.StringType, 'required' : False },
                       }

    def init(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.

        Находим домен по пути из корневого.
        """
        def doIt(_):
            try:
                self.model = self.domain.get(self.params.model)
            except DomainKeyError:
                raise errors.AttributeKeyException, self.params.model

            if not IModel.providedBy(self.model):
                raise errors.NotAModelError, self.params.model

            self.message = self.params.message.getMessage(self.domain)

            if self.params.text_attribute is None:
                self.params.text_attribute = 'text'

            try:
                self.text = self.message[self.params.text_attribute].value()
            except AttributeNotFoundError:
                raise errors.MessageAttributeKeyException, self.params.text_attribute

        return defer.maybeDeferred(super(ModelBaseCommand, self).init).addCallback(doIt)



