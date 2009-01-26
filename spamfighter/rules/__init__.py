# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Набор правил анализа сообщений СпамоБорца.
"""

def loadRules():
    """
    Загрузить все правила СпамоБорца.
    """

    from twisted.python import modules

    module = modules.getModule(__name__)
    for mod in module.walkModules():
        mod.load()


