# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команды с поддержкой выбора партнера и домена.
"""

import types
import time
from zope.interface import implements
from twisted.internet import defer

from spamfighter.core.commands.command import Command
from spamfighter.core.commands.serialize import ISerializable, register_serializer
from spamfighter.core.commands import errors
from spamfighter.core.partner import getPartnerAuthorizer, PartnerAuthorizationFailedError
from spamfighter.core.domain import DomainPathError

class IPartnerAuthInfo(ISerializable):
    """
    Информация об авторизации партнера.
    """

class PartnerAuthInfo(object):
    """
    Класс, хранящий информации об авторизации партнера.

    @ivar info: инорфмация об авторизации (произвольного типа)
    """
    implements(IPartnerAuthInfo)
    register_serializer(IPartnerAuthInfo)

    def __init__(self, info):
        """
        Конструктор.

        @param info: инорфмация об авторизации (произвольного типа)
        """
        self.info = info

    def serialize(self):
        """
        Сериализация.
        """
        return self.info

    @classmethod
    def unserialize(cls, serialized):
        """
        Десериализация.
        """
        return PartnerAuthInfo(serialized)

class CommandParamMergerMeta(type):
    """
    Мета-тип, который собирает вместе сигнатуру
    команд по цепочке наследования классов.
    """
    def __init__(cls, name, bases, dict):
        """
        Собираем вместе C{commandSignature} от всех предков и от нашего класса.
        """
        super(CommandParamMergerMeta, cls).__init__(name, bases, dict)
        def updateCommandSignature(cS, item):
            cS.update(getattr(item, 'commandSignature', {}))
            return cS
        commandSignature = reduce(updateCommandSignature, bases + (cls, ), {})
        setattr(cls, 'commandSignature', commandSignature)

class PartneredCommand(Command):
    """
    Команда, обязательным параметром которой является партнер.
    Команда автоматически осуществляет авторизацию партнера.

    @ivar partner: партнер, авторизованный для данной команды
    @type partner: L{spamfighter.interfaces.IPartner}
    """
    __metaclass__ = CommandParamMergerMeta

    commandSignature = {
            'partner' : { 'type' : IPartnerAuthInfo, 'required' : True}, 
                       }

    def init(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.

        Определяем партнера по механизму авторизации партнеров.
        """
        def authFailed(failure):
            failure.trap(PartnerAuthorizationFailedError)
            raise errors.AuthorizationFailedException

        def authOk(partner):
            self.partner = partner

        return getPartnerAuthorizer().authorize(self.params.partner.info).addErrback(authFailed).addCallback(authOk)
        
class DomainedCommand(PartneredCommand):
    """
    Команда, которая в качестве параметра может содержать путь к поддомену,
    относительно которого она будет выполняться. Поддомен вычисляется относительно
    корневого домена партнера.

    @ivar domain: домен, относительно которого выполняется комананда
    @type domain: L{spamfighter.interfaces.IDomain}
    @ivar startTime: время начала обработки команды
    @type startTime: C{float}
    """
    commandSignature = {
            'domain' : { 'type' : types.StringType, 'required' : False}, 
                       }

    def init(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.

        Находим домен по пути из корневого.
        """
        def doIt(_):
            self.startTime = time.time()

            def gotRootDomain(domain):
                self.domain = domain

                if self.params.domain is not None:
                    def gotDomain(domain):
                        self.domain = domain

                    def handleDomainPathError(failure):
                        failure.trap(DomainPathError)
                        raise errors.DomainPathNotFoundException, failure.value.args[0]

                    return self.domain.walk(self.params.domain).addCallback(gotDomain).addErrback(handleDomainPathError)

            return self.partner.rootDomain().addCallback(gotRootDomain) 

        return defer.maybeDeferred(super(DomainedCommand, self).init).addCallback(doIt)

    def finalize(self):
        """
        Дополнительный метод, может переопределяться в потомках для выполнения завершения
        обработки команды.

        Обновляем счетчики.
        """
        serviceTime = time.time() - self.startTime

        domain = self.domain
        while domain is not None:
            if domain.has('counterRequest'):
                domain.get('counterRequest').increment()
            if domain.has('counterRPS'):
                domain.get('counterRPS').increment()
            if domain.has('counterAST'):
                domain.get('counterAST').increment(serviceTime)

            domain = domain.parent()

