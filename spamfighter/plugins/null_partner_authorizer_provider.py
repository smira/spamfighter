# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Плагин, реализующий авторизацию партнеров без логинов/паролей (доверительный вариант).
"""

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.plugin import IPartnerAuthorizerProvider
from spamfighter.core.null_partner import NullPartnerAuthorizer

class NullPartnerAuthorizerProvider(object):
    """
    Провайдер авторизации партнеров без логинов/паролей.
    """
    implements(IPlugin, IPartnerAuthorizerProvider)

    def __init__(self):
        """
        Конструктор.
        """

    def name(self):
        """
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return 'NullPartnerAuthorizerProvider'

    def getPartnerAuthorizer(self):
        """
        Получить механизм авторизации партнеров.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
        """
        return NullPartnerAuthorizer()

nullPartnerAuthorizer = NullPartnerAuthorizerProvider()

