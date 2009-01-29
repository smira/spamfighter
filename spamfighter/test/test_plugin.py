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
Тесты на L{spamfighter.plugin}.
"""

import unittest

from spamfighter import plugin
from spamfighter.test.plugins import ITestPlugin1, ITestPlugin2, ITestPlugin3
import spamfighter.test.plugins

class PluginTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugin.loadPlugin}.
    """

    def testLoadPlugin(self):
        plug1 = plugin.loadPlugin(ITestPlugin1, 'testplugin1', spamfighter.test.plugins)
        self.assert_(ITestPlugin1.providedBy(plug1))
        self.assertEqual('testplugin1', plug1.name())

        plug2 = plugin.loadPlugin(ITestPlugin1, 'testplugin2', spamfighter.test.plugins)
        self.assert_(ITestPlugin1.providedBy(plug2))
        self.assert_(ITestPlugin2.providedBy(plug2))
        self.assertEqual('testplugin2', plug2.name())

    def testLoadPluginNotFound(self):
        self.assertRaises(plugin.PluginNotFoundError, plugin.loadPlugin, ITestPlugin1, 'testplugin45', spamfighter.test.plugins)
        self.assertRaises(plugin.PluginNotFoundError, plugin.loadPlugin, ITestPlugin3, 'testplugin1', spamfighter.test.plugins)

    def testLoadPluginAmbiguity(self):
        self.assertRaises(plugin.PluginAmbiguityError, plugin.loadPlugin, ITestPlugin2, 'testplugin3', spamfighter.test.plugins)
