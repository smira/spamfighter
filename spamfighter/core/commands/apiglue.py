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
"Клей", позволяющий приклеить нашу систему команд к Twisted-варианту XML-RPC & JSON-RPC.
"""

import sys
from functools import update_wrapper

import xmlrpclib
from twisted.web import xmlrpc
from twisted.python import log

from spamfighter.txjsonrpc import jsonrpclib
from spamfighter.txjsonrpc.web import jsonrpc

from spamfighter.core.commands import errors
from spamfighter.core.commands.dispatcher import dispatchCommand

def build_error_translator(faultClass):
    """
    Построить декоратор, транслирующий наши исключения в исключения Fault для JSON-RPC/XML-RPC.
    """

    def error_translator(f, deferred=False):
        """
        Собственно декоратор, транслирующий наши исключения в исключения Fault для JSON-RPC/XML-RPC.

        Если это наше исключение (из L{spamfighter.core.commands.errors}), переводим
        его в соответствующий Fault, иначе создаем Fault для 
        L{spamfighter.core.commands.errors.UnexpectedException}.

        @param deferred: обрабатывать ли исключения в Deferred-возврате?
        @type deferred: C{bool}
        """
        def translator(*args, **kw):
            try:
                def translateBaseDeferredError(failure):
                    failure.trap(errors.BaseCommandException)
                    raise faultClass(failure.value.getCode(), failure.value.getMessage())

                def translateUnknownDeferredError(failure):
                    if failure.check(faultClass) is faultClass:
                        return failure

                    if not sys.modules.has_key('twisted.trial.runner'):
                        log.err(failure)

                    e = errors.UnexpectedException()
                    raise faultClass(e.getCode(), e.getMessage())
                
                if deferred:
                    return f(*args, **kw).addErrback(translateBaseDeferredError).addErrback(translateUnknownDeferredError)
                else:
                    return f(*args, **kw)
            except errors.BaseCommandException, e:
                raise faultClass(e.getCode(), e.getMessage())
            except:
                if not sys.modules.has_key('twisted.trial.runner'):
                    log.err()

                e = errors.UnexpectedException()
                raise faultClass(e.getCode(), e.getMessage())

        return update_wrapper(translator, f)

    return error_translator

jsonrpc_error_translator = build_error_translator(jsonrpclib.Fault)
xmlrpc_error_translator = build_error_translator(xmlrpclib.Fault)

class API_Glue:
    """
    Базовый класс, обеспечивающий связь XML-RPC и JSON-RPC реализаций на базе
    Twisted.Web с нашей системой команд.

    Данный вариант является базовым и зависит от типа используемого
    преобразователя ошибок (для XML-RPC или JSON-RPC).
    """

    def _internalGetFunction(self, error_translator, functionPath):
        """
        Получить функцию, выполняющую команду с указанным именем и при этом
        использующую указанный механизм преобразования ошибок.

        @param error_translator: преобразователь ошибок
        @param functionPath: имя функции (полное, как путь)
        @type functionPath: C{str}
        @return: функция, которая принимает параметры команды и возвращает Deferred на её результат
        """
        command = dispatchCommand(functionPath)
        
        def commandAsMethod(params):
            try:
                command.params.getUnserialized(params)
            except AttributeError, (param):
                raise errors.UnknownParameterException, param
            except TypeError, (param):
                raise errors.TypeParameterException, param

            return command.run().addCallback(lambda _: command.getResponse())

        return error_translator(commandAsMethod, deferred=True)

class JSONRPC_API_Glue(jsonrpc.JSONRPC, API_Glue):
    """
    Ресурс JSON-RPC (Twisted Web), который обрабатывает команды нашего API (минуя стандартные механизмы поиска функции).
    """
    @jsonrpc_error_translator
    def _getFunction(self, functionPath):
        return self._internalGetFunction(jsonrpc_error_translator, functionPath)

class XMLRPC_API_Glue(xmlrpc.XMLRPC, API_Glue):
    """
    Ресурс XML-RPC (Twisted Web), который обрабатывает команды нашего API (минуя стандартные механизмы поиска функции).
    """
    @xmlrpc_error_translator
    def _getFunction(self, functionPath):
        return self._internalGetFunction(xmlrpc_error_translator, functionPath)


