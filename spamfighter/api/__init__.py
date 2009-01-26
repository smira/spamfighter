# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Набор команд, составляющих API СпамоБорца (C{sf.*}).
"""

def loadCommands():
    """
    Загрузить все команды СпамоБорца.
    """

    from twisted.python import modules

    module = modules.getModule(__name__)
    for mod in module.walkModules():
        mod.load()



