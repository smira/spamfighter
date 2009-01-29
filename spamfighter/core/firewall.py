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
"Черный ящик" анализа сообщений по правилам, построенный
по мотивам работы firewall.
"""

from zope.interface import implements
from twisted.internet import defer
from twisted.python import failure

from spamfighter.interfaces import IMessage, IMessageAnalyzer, ITaggedMessage, IMessageFirewall
from spamfighter.core.rules import factory as rulesFactory
from spamfighter.core.commands import errors
from spamfighter.core.message import TaggedMessage, AttributeNotFoundError
from spamfighter.core.domain import DomainKeyError

# Грамматика нашего firewall
from pyparsing import Literal, Word, alphanums, nums, delimitedList, OneOrMore, Optional, Group, Suppress, ParseException, CharsNotIn

# Отдельные элементы
gTag = Word(alphanums+'_')
gTagList = delimitedList(gTag)
gLabel = Word(nums)
gResultLabel = Word(alphanums)
gFunctionName = Word(alphanums)
gParamName = Word(alphanums)
gValueInt = Word(nums).setParseAction(lambda value: int(value[0]))
gValueString = Suppress(Literal('"')) + CharsNotIn('"') + Suppress(Literal('"'))
gParamValue = gValueInt | gValueString
gFunctionParam = Group(gParamName + Suppress(Literal('=')) + gParamValue)

# Куски отдельных правил
gIfClause = Literal("if") + Optional(Literal("not").setResultsName('inverted_if')) + gTagList.setResultsName('if_tags')
gMarkClause = Literal("mark") + gTagList.setResultsName('markers')
gLabelClause = gLabel.setResultsName('label') + Literal(':')
gRuleCall = gFunctionName.setResultsName('function_name') + Literal("(") + Optional(delimitedList(gFunctionParam).setResultsName('function_args')) + Literal(")")

# skip to 345
gSkipToClause = Literal("skip").setResultsName('statement') + Suppress(Literal("to")) + gLabel.setResultsName('skip_to_label')

# do checkMessageLength(max=110,aaa='aaa') mark ok
gDoClause = Literal("do").setResultsName('statement') + gRuleCall + Optional(gMarkClause)

# stop as SPAM 
gStopClause = Literal("stop").setResultsName('statement') + Suppress(Literal("as")) + gResultLabel.setResultsName('stop_marker')

gOneOfStatements = gSkipToClause | gDoClause | gStopClause
gStatement = Optional(gLabelClause) + Optional(gIfClause) + gOneOfStatements
gRuleset = OneOrMore(Group(gStatement))

class SyntaxError(Exception):
    """
    Сообщение об ошибке в синтаксисе файрвола.
    """

class SkipToProcess(Exception):
    """
    Служебное исключение, используется для "пропуска" правил
    в файрволе.

    @ivar label: лейбл, до которого мы должны пропускать правила
    @type label: C{int}
    @ivar pack: информация о обрабатываемом сообщении
    @type pack: C{FirewallMessagePack}
    """
    
    def __init__(self, label, pack):
        """
        Конструктор.
        """
        self.label = label
        self.pack = pack

    def __repr__(self):
        return 'SkipToProcess(%d, %r)' % (self.label, self.pack)

    def __str(self):
        return 'Skipping until label %d' % (self.label)

class FirewallMessagePack(object):
    """
    Объект, оборачивающий в один параметр Deferred все данные,
    необходимые при обработке сообщения.

    @ivar message: сообщение
    @type message: L{ITaggedMessage}
    @ivar domain: текущий домен
    @type domain: L{IDomain}
    """

    def __init__(self, message, domain):
        """
        Конструктор.
        """
        self.message = message
        self.domain = domain

    def debug(self, message):
        """
        Добавить в лог отладочное сообщение.

        В процессе движения по firewall в отладочном режиме собирается лог
        сообщений, описывающий процесс прохождения отдельных действий.

        @param message: отладочное сообщение
        @type message: C{str}
        """
        if not hasattr(self, "log"):
            self.log = []

        self.log.append(message)

    def getLog(self):
        """
        Получить текущий собранный отладочный лог.

        @return: лог сообщений
        @rtype: C{list(str)}
        """
        return getattr(self, "log", [])

class FirewallStatement(object):
    """
    Класс, инкаспилирующий одно правило файрвола.

    Конкретные наследники реализуют конкретные правила.

    @ivar if_tags: набор тегов, по которым идёт фильтрация применения правила
    @type if_tags: C{list}
    @ivar if_inverted: инвертированный смысл условия по if (if not?)
    @type if_inverted: C{bool}
    @ivar label: метка правила
    @type label: C{int}
    """

    def __init__(self, if_tags=None, if_inverted=False, label=None):
        """
        Конструктор.

        @param if_tags: набор тегов, по которым идёт фильтрация применения правила
        @type if_tags: C{list}
        @param if_inverted: инвертированный смысл условия по if (if not?)
        @type if_inverted: C{bool}
        @param label: метка правила
        @type label: C{int}
        """
        self.if_tags = if_tags
        self.if_inverted = if_inverted
        self.label = label

    def __eq__(self, other):
        return self.if_tags == other.if_tags and self.if_inverted == other.if_inverted and \
                self.label == other.label

    def __repr__(self):
        return "if_tags=%r, if_inverted=%r, label=%r" % (self.if_tags, self.if_inverted, self.label)

    def __str__(self):
        """
        Получить строковое представление правила (в исходной грамматике).

        @rtype: C{str}
        """
        result = ''
        if self.label is not None:
            result += "%d: " % self.label
        if self.if_tags is not None:
            result += "if %s%s " % ("not " if self.if_inverted else "", ", ".join(self.if_tags))

        return result

    def compile(self, d, debug=False):
        """
        Скомпилировать правило, присоединив его к цепочке deferred.

        @param d: цепочка отложенных вызовов
        @type d: C{twisted.internet.defer.Deferred}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        if self.label is not None:
            d.addErrback(self._label_helper, debug)

        if debug:
            def enterRule(pack):
                pack.debug("[ENTER]: %s" % self)
                return pack
            d.addCallback(enterRule)
        return d

    def _if_helper(self, message):
        """
        Элемент цепочки отложенных вызовов, отвечающий за обработку условия.

        @param message: обрабатываемое сообщение
        @type message: L{ITaggedMessage}
        @return: результат обработки сообщения
        @rtype: C{bool}
        """
        if self.if_tags is None:
            return True

        if self.if_inverted and not message.checkHasNoTags(self.if_tags):
            return False
        if not self.if_inverted and not message.checkHasAllTags(self.if_tags):
            return False

        return True

    def _label_helper(self, failure, debug=False):
        """
        Errback, который ловит L{SkipToProcess}, чтобы обеcпечить остановку
        на нужном label после skip to.
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        failure.trap(SkipToProcess)

        if failure.value.label != self.label:
            if debug:
                failure.value.pack.debug("Labels for skip don't match %d != %d" % (failure.value.label, self.label))
            return failure

        if debug:
            failure.value.pack.debug("Stopped skip to at label %d" % self.label)

        return failure.value.pack

class SkipFirewallStatement(FirewallStatement):
    """
    Реализация правила 'skip to ...'.

    @ivar skip_label: лейбл, до которого пропускать правила
    @type skip_label: C{int}
    """

    def __init__(self, skip_label, **kwargs):
        """
        Конструктор.
        """
        super(SkipFirewallStatement, self).__init__(**kwargs)
        self.skip_label = skip_label

    def __eq__(self, other):
        return super(SkipFirewallStatement, self).__eq__(other) and self.skip_label == other.skip_label

    def __repr__(self):
        return "SkipFirewallStatement(skip_label=%r, %s)" % (self.skip_label, super(SkipFirewallStatement, self).__repr__())

    def __str__(self):
        """
        Получить строковое представление правила (в исходной грамматике).

        @rtype: C{str}
        """
        return super(SkipFirewallStatement, self).__str__() + ("skip to %d" % self.skip_label)

    def compile(self, d, debug=False):
        """
        Скомпилировать правило, присоединив его к цепочке deferred.

        @param d: цепочка отложенных вызовов
        @type d: C{twisted.internet.defer.Deferred}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        return super(SkipFirewallStatement, self).compile(d, debug).addCallback(self._skipto_helper, debug)

    def _skipto_helper(self, pack, debug=False):
        """
        Callback, который обеспечивает выполнение skip to (если if-часть позволяет это).

        @param pack: информация о обрабатываемом сообщении
        @type pack: C{FirewallMessagePack}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        if self._if_helper(pack.message):
            if debug:
                pack.debug("Skipping to %d" % self.skip_label)
            return failure.Failure(SkipToProcess(self.skip_label, pack))

        return pack

class StopFirewallStatement(FirewallStatement):
    """
    Реализация правила 'stop as...'

    @ivar stop_marker: маркер результата обработки
    @type stop_marker: C{str}
    """

    def __init__(self, stop_marker, **kwargs):
        """
        Конструктор.
        """
        super(StopFirewallStatement, self).__init__(**kwargs)
        self.stop_marker = stop_marker

    def __eq__(self, other):
        return super(StopFirewallStatement, self).__eq__(other) and self.stop_marker == other.stop_marker

    def __repr__(self):
        return "StopFirewallStatement(stop_marker=%r, %s)" % (self.stop_marker, super(StopFirewallStatement, self).__repr__())

    def __str__(self):
        """
        Получить строковое представление правила (в исходной грамматике).

        @rtype: C{str}
        """
        return super(StopFirewallStatement, self).__str__() + ("stop as %s" % self.stop_marker)

    def compile(self, d, debug=False):
        """
        Скомпилировать правило, присоединив его к цепочке deferred.

        @param d: цепочка отложенных вызовов
        @type d: C{twisted.internet.defer.Deferred}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        return super(StopFirewallStatement, self).compile(d, debug).addCallback(self._stop_helper, debug)

    def _stop_helper(self, pack, debug=False):
        """
        Callback, который останавливает обработку правил файрвола с
        указанием результата (если if-часть разрешает это).

        @param pack: информация о обрабатываемом сообщении
        @type pack: C{FirewallMessagePack}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        if self._if_helper(pack.message):
            if debug:
                pack.debug("Stopping firewall with result: %s" % self.stop_marker)
            return failure.Failure(FirewallResult(self.stop_marker))

        return pack

class DoFirewallStatement(FirewallStatement):
    """
    Реализация правила "do ... mark as ..."

    @ivar func: частично определенный вызов функции обработки сообщения
    @type func: C{func}
    @ivar func_name: имя вызываемого правила
    @type func_name: C{str}
    @ivar func_args: аргументы правила
    @type func_args: C{dict}
    @ivar markers: список тегов, которыми надо пометить сообщение в случае "успешной" обработки
    @type markers: C{list(str)}
    """

    def __init__(self, func_name, func_args, markers=None, **kwargs):
        """
        Конструктор.

        @param func_name: имя вызываемого правила
        @type func_name: C{str}
        @param func_args: аргументы правила
        @type func_args: C{dict}
        @param markers: теги, которыми надо пометеить сообщение в случае "успешной" обработки
        @type markers: C{list(str)}
        """
        super(DoFirewallStatement, self).__init__(**kwargs)
        self.func_name = func_name
        self.func_args = func_args
        self.func = rulesFactory.instanciateRule(func_name, **func_args)
        self.markers = markers

    def __eq__(self, other):
        return super(DoFirewallStatement, self).__eq__(other) and self.markers == other.markers and \
                self.func_name == other.func_name and self.func_args == other.func_args

    def __repr__(self):
        return "DoFirewallStatement(func_name=%r, func_args=%r, markers=%r, %s)" % (self.func_name, \
                self.func_args, self.markers, super(DoFirewallStatement, self).__repr__())

    def __str__(self):
        """
        Получить строковое представление правила (в исходной грамматике).

        @rtype: C{str}
        """
        result = super(DoFirewallStatement, self).__str__() + "do %s(%s)" % (self.func_name, ", ".join(["%s=%r" % (name, value) for name, value in self.func_args.items()]))
        if self.markers is not None:
            result += " mark %s" % ", ".join(self.markers)

        return result

    def compile(self, d, debug=False):
        """
        Скомпилировать правило, присоединив его к цепочке deferred.

        @param d: цепочка отложенных вызовов
        @type d: C{twisted.internet.defer.Deferred}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        return super(DoFirewallStatement, self).compile(d, debug).addCallback(self._do_helper, debug)

    def _do_helper(self, pack, debug=False):
        """
        @param pack: информация о обрабатываемом сообщении
        @type pack: C{FirewallMessagePack}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        """
        if self._if_helper(pack.message):
            d = defer.maybeDeferred(self.func, message=pack.message, domain=pack.domain)
            def markMessage(result):
                if debug:
                    pack.debug("Result: %r" % result)

                if not result and self.markers is not None:
                    for tag in self.markers:
                        pack.message.addTag(tag)
                    if debug:
                        pack.debug("Tagged message with tags: %r, current tags are: %r" % (self.markers, pack.message.getTags()))
                
                return pack

            d.addCallback(markMessage)
            return d

        return pack

class FirewallResult(Exception):
    """
    Служебное исключение, обработка цепочки правил
    закончилась результатом.

    @ivar result: результат обработки
    @type result: C{str}
    """

    def __init__(self, result):
        """
        Конструктор.
        """
        self.result = result

    def __str__(self):
        return "stop as %s" % self.result

class MessageFirewall(object):
    """
    "Черный ящик" анализа сообщений по правилам, построенный
    по мотивам работы firewall.

    @ivar rules: текущие правила анализа (текстовое представление)
    @type rules: C{str}
    @ivar compiled: скомпилированные правила анализа
    @type compiled: C{list(}L{FirewallStatement}C{)}
    """
    implements(IMessageAnalyzer, IMessageFirewall)

    def __init__(self, rules=None):
        """
        Конструктор.

        @param rules: правила анализа
        @type rules: C{str}
        """
        self.rules = None
        self.compiled = []
        self.setRules(rules)

    def __getstate__(self):
        return { 'rules' : self.rules }

    def __setstate__(self, state):
        self.__init__(state['rules'])
    
    def getRules(self):
        """
        Получить текущие правила firewall'а.

        @return: текстовое представление текущих правил.
        @rtype: C{str}
        """
        if self.rules is None:
            return ''
        return self.rules

    def setRules(self, rules):
        """
        Установить новые правила анализа.

        @param rules: правила анализа
        @type rules: C{str}
        """
        if rules is None:
            self.rules = None
            self.compiled = []
        else:
            self.compiled = self.compile(self.parse(rules))
            self.rules = rules

    def syntaxCheck(self, rules):
        """
        Осуществить синтаксическую проверку текста правил.

        @param rules: правила анализа
        @type rules: C{str}
        @raises SyntaxError: если записи правил имеются синтаксические ошибки
        """
        self.parse(rules)

    def parse(self, rules):
        """
        Распарсить текстовую запись правил файрвола и вернуть
        синтаксически корректное внутреннее представление.

        @param rules: правила файрвола (в виде текста)
        @type rules: C{str}
        @return: распознанное представление
        @rtype: C{list}
        @raises SyntaxError: если записи правил имеются синтаксические ошибки
        """
        global gRuleset

        try:
            return gRuleset.parseString(rules, parseAll=True)
        except ParseException, e:
            raise SyntaxError, str(e)

    def compile(self, parsed_rules):
        """
        Компиляция распарсенного представления правил в 
        набор объектов правил файрвола.

        @param parsed_rules: распознанное представление правил
        @type parsed_rules: C{list}
        """
        def transformRule(rule):
            kwargs = {}

            if rule.if_tags != '':
                kwargs['if_tags'] = list(rule.if_tags)
                if rule.inverted_if == 'not':
                    kwargs['if_inverted'] = True
                else:
                    kwargs['if_inverted'] = False
            if rule.label != '':
                kwargs['label'] = int(rule.label)

            if rule.statement == 'skip':
                return SkipFirewallStatement(skip_label=int(rule.skip_to_label), **kwargs)
            elif rule.statement == 'do':
                if rule.markers != '':
                    markers = list(rule.markers)
                else:
                    markers = None
                return DoFirewallStatement(func_name=rule.function_name, 
                        func_args=dict(list(map(lambda l: list(l), rule.function_args))), markers=markers, **kwargs)
            elif rule.statement == 'stop':
                return StopFirewallStatement(stop_marker=rule.stop_marker, **kwargs)
            else:
                assert False

        return map(transformRule, parsed_rules)

    def analyze(self, message, domain, debug=False, logCallback=None):
        """
        Анализировать входящие сообщение и вернуть результат анализа.

        @param message: анализируемое сообщение
        @type message: L{IMessage}
        @param domain: текущий домен
        @type domain: L{IDomain}
        @return: результат анализа
        @rtype: C{twisted.internet.defer.Deferred}
        @param debug: включить отладочный режим?
        @type debug: C{bool}
        @param logCallback: функция, которая получит лог прохождения сообщения
                            через firewall в отладочном режиме, прототип функции:
                            С{logCallback(log)}
        """
        if not ITaggedMessage.providedBy(message):
            message = TaggedMessage(message=message)
        pack = FirewallMessagePack(message, domain)
        d = defer.succeed(pack)
        for statement in self.compiled:
            statement.compile(d, debug)
        d.addCallback(lambda _: 'UNKNOWN') # если ни одно правило не завершилось stop as, считаем результат неизвестным
        
        def processStop(failure):
            """
            Обрабатываем обычный случай завершения обработки через stop as..
            """         
            failure.trap(FirewallResult)
            return failure.value.result
        d.addErrback(processStop)

        def processSkipThrough(failure):
            """
            Обрабатываем ситуацию, когда для skip to.. не нашлось метки.
            """
            failure.trap(SkipToProcess)
            raise errors.SkipToFallthroughError(failure.value.label)
        d.addErrback(processSkipThrough)

        def handleDomainKeyError(failure):
            """
            Обрабатываем отсутствующий ключ в домене, на который "напоролось" правило.
            """
            failure.trap(DomainKeyError)
            raise errors.AttributeKeyException, failure.value.args[0]
        d.addErrback(handleDomainKeyError)


        def handleAttributeKeyError(failure):
            """
            Обрабатываем исключение об отсутствии атрибута у сообщения.
            """
            failure.trap(AttributeNotFoundError)
            raise errors.MessageAttributeKeyException, failure.value.args[0]
        d.addErrback(handleAttributeKeyError)
        
        if debug:
            def returnLog(res):
                logCallback(pack.getLog())
                return res

            d.addBoth(returnLog)

        return d

