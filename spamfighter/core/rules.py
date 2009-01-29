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
Обслуживание правил для анализа сообщений.
"""

import types
from functools import partial

class DuplicateRuleError(Exception):
    """
    Правило с таким именем уже было зарегистриовано.
    """

class RuleNotFoundError(Exception):
    """
    Правило с таким именем не найдено.
    """

class RulesFactory(object):
    """
    Фабрика правил анализа сообщений. Регистрирует правила
    и выдает их по требованию.

    Правило анализа сообщений может быть:
     - функцией
     - классом

    В случае функции правило должно иметь вид::
      def rule(domain, message, arg1, arg2=33)

    где:
     - C{domain} (L{spamfighter.interfaces.IDomain}) - текущий домен;
     - C{message} (L{spamfighter.interfaces.IMessage}) - обрабатываемое сообщение;
     - C{arg1}, C{arg2} - дополнительные параметры правил анализа;
     - именем правила будет имя функции (C{rule}).

    Класс должен иметь следующий вид::
      class Rule(object):
          def __init__(self, arg1, arg2=33):
             ...
          def analyze(domain, message):
             ...

    Смысл полей аналогично случаю функции, именем правила будет имя класса.

    @ivar rules: хэш по имени зарегистрированных правил
    @type rules: C{dict}
    """

    def __init__(self):
        """
        Конструктор.
        """
        self.rules = {}

    def registerRule(self, rule):
        """
        Добавить новое правило (зарегистрировать).

        @param rule: новое правило
        @type rule: C{func} или C{class}
        @raise DuplicateRuleError: если правило с таким же именем уже было зарегистрировано
        """
        if type(rule) is types.FunctionType:
            name = rule.func_name 
            info = { 'class' : None, 'method' : rule }
        else:
            name = rule.__name__
            info = { 'class' : rule, 'method' : rule.analyze }
        
        if self.rules.has_key(name):
            raise DuplicateRuleError, name

        self.rules[name] = info

    def unregisterRule(self, rule):
        """
        Удалить ранее зарегистрированное правило.

        @param rule: новое правило
        @type rule: C{func} или C{class}
        @raise RuleNotFoundError: правило с указанным имененем не обнаружено
        """
        if type(rule) is types.FunctionType:
            name = rule.func_name 
        else:
            name = rule.__name__

        if not self.rules.has_key(name):
            raise RuleNotFoundError, name

        del self.rules[name]

    def instanciateRule(self, name, **kwargs):
        """
        Инстанциировать правило, создать его экземпляр с указанными параметрами.

        Возвращает функцию, в которой должно остаться только два свободных параметра:
        домен и сообщение.

        @param name: имя правила
        @type name: C{str}
        @return: инстанциированное правило
        @rtype: C{func}
        @raise RuleNotFoundError: правило с указанным имененем не обнаружено
        """
        if not self.rules.has_key(name):
            raise RuleNotFoundError, name

        if self.rules[name]['class'] is None:
            return partial(self.rules[name]['method'], **kwargs)
        else:
            return partial(self.rules[name]['method'], self.rules[name]['class'](**kwargs))

    def getRuleNames(self):
        """
        Получить имена всех правил.

        @return: список имен правил
        @rtype: C{list(str)}
        """
        return self.rules.keys()

factory = RulesFactory()

def ruleTrue(domain, message):
    """
    Правило, которое всегда возвращает истину.
    """
    return True

def ruleFalse(domain, message):
    """
    Правило, которое всегда возвращает ложь.
    """
    return False

factory.registerRule(ruleTrue)
factory.registerRule(ruleFalse)
