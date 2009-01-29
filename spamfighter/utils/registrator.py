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
Декоратор регистрации, позволяющий получить текущий класс в функции,
вызванной в теле класса.
"""

def registrator(f):
    """Декоратор регистраторов

    оборачивает методы которые затем могут вызываться в определении классов.
    При этом первым параметром в оборачиваемую функцию передается класс в определении которого она вызвана

    Пример::

        @registrator
        def register(cls, *args, **kw):
            print "Class:", cls

        class Test(object):
            register()

    выведет на экран 
    <class '__main__.Test'>
    """
    def registration(*args, **kw):
        _implements(f.__name__, args, kw , f)

    return registration

import sys
from zope.interface.advice import addClassAdvisor

def _implements(name, args, kw, classImplements):

    #NOTE: str(classImplements) в данном случае используется просто в качестве уникального идентификатора

    def _implements_advice(cls):
        classImplements(cls, *args, **kw)
        return cls

    frame = sys._getframe(2)
    locals = frame.f_locals
    # Try to make sure we were called from a class def. In 2.2.0 we can't
    # check for __module__ since it doesn't seem to be added to the locals
    # until later on.
    if (locals is frame.f_globals) or (
        ('__module__' not in locals) and sys.version_info[:3] > (2, 2, 0)):
        raise TypeError(name+" can be used only from a class definition.")
    if str(classImplements) in locals:
        raise TypeError(name+" can be used only once in a class definition.")
    locals[str(classImplements)] = args, kw, classImplements
    addClassAdvisor(_implements_advice, depth=3)
