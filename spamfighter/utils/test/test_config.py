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
Тесты на L{spamfighter.utils.config}.
"""

import os.path
import inspect
import unittest
from spamfighter.utils.config import _load_file


class ConfigTestCase(unittest.TestCase):
    """
    Тесты на L{spamfighter.utils.config}.
    """

    def testLoadFile(self):
        config = _load_file(os.path.join(os.path.dirname(inspect.getfile(ConfigTestCase)), 'test_config.xml'))

        self.assertEquals("34", config.aaaa.bbb)
        self.assertEquals(3, config.aaaa.ccc)

        self.assertEquals("c", config.override.nooverride)
        self.assertEquals("B", config.override.doit)

        self.assertEquals("3", config.override.nextlevel)

        self.assertEquals("10", config.override.thirdlevel)

        self.assertEquals("A", config.included)
