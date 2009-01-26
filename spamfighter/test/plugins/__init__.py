# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Плагины для тестов.
"""

from spamfighter.plugin import INamedPlugin

class ITestPlugin1(INamedPlugin):
    """
    Интерфейс тестовых плагинов #1.
    """

class ITestPlugin2(INamedPlugin):
    """
    Интерфейс тестовых плагинов #2.
    """

class ITestPlugin3(INamedPlugin):
    """
    Интерфейс тестовых плагинов #3.
    """
