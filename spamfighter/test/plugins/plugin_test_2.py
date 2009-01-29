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

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.test.plugins import ITestPlugin1, ITestPlugin2

class TestPlugin2(object):
    implements(IPlugin, ITestPlugin1, ITestPlugin2)

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

plugin1 = TestPlugin2('testplugin2')
plugin2 = TestPlugin2('testplugin3')
plugin3 = TestPlugin2('testplugin3')

