# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Диспетчеризация команд по имени.

Т.е. отображаем имя команды (атрибут comandName из интерфейса L{spamfighter.core.commands.ICommand}) в
класс команды.
"""

from spamfighter.utils.registrator import registrator
from spamfighter.core.commands import errors

dispatch_map = {}
"""
Карта отображения команд, имеет вид: имя_команды -> класс_команды.
"""

@registrator
def install(command_class):
    """Вариант функции L{installCommand} которую можно использовать в определении класса

    Пример использования::
        from spamfighter.core.commands import install, Command
        class MyCommand(Command):
            install()
    """
    installCommand(command_class)

def installCommand(command_class):
    """Установить новую команду в карту диспетчеризации.

    @param command_class: класс, производный от L{Command}
    """
    name = command_class.commandName

    assert name not in dispatch_map

    dispatch_map[name] = command_class

def deinstallCommand(command_class):
    """
    Убрать команду из карты диспетчеризации.


    @param command_class: класс, производный от L{Command}
    """
    name = command_class.commandName

    assert name in dispatch_map

    del dispatch_map[name]

def dispatchCommand(commandName):
    """
    Найти класс команды, соответствующий данной команде по имени

    @param commandName: имя команды
    @type commandName: C{str}
    @raise errors.CommandUnknownException: если такой команды не существует
    @rtype: производная от L{Command}
    """
    if commandName not in dispatch_map:
        raise errors.CommandUnknownException, commandName

    return dispatch_map[commandName]()

def listAllCommands():
    """
    Вернуть список всех команд.
    """
    return dispatch_map.keys()
