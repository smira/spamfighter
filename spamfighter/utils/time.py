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
Модуль подсчета "неточного" времени (разрешение одна секунда). Доступен
вариант для использования в unit-тестах.

Модуль экспортирует функцию C{time()}, которая возвращает целое число
секунд, начиная с некоторой даты. В production - это переменная, которая
обновляется (осуществляется системный вызов) не чаще, чем раз в секунду.

При использовании в тестах можно подменить реальное время модельным.
После вызова функции startUpTestTimer функция time() буде возвращать таймер,
значение которого можно корректировать
"""

import sys
from ..time import time as sys_time

from twisted.internet import reactor

def _inaccurate_time():
    return _inaccurate_timer

_timer_func = _inaccurate_time

_inaccurate_timer = int(sys_time())

def time():
    return _timer_func()

def _inaccurate_timer_tick():
    global _inaccurate_timer
    _inaccurate_timer = int(sys_time())

    _start_inaccurate_timer()

def _start_inaccurate_timer():
    if not sys.modules.has_key('twisted.trial.runner'):
        reactor.callLater(1, _inaccurate_timer_tick)

_start_inaccurate_timer()

_test_timer = 0

def _test_time():
    return _test_timer

def startUpTestTimer(initial = 0):
    global _timer_func, _test_timer

    _test_timer = initial
    _timer_func = _test_time

def advanceTestTimer(step):
    global _test_timer

    _test_timer += step

def setTestTimer(value):
    global _test_timer

    _test_timer = value

def tearDownTestTimer():
    global _timer_func

    _timer_func = _inaccurate_time

__all__ = ['time', 'startUpTestTimer', 'advanceTestTimer', 'setTestTimer', 'tearDownTestTimer']

