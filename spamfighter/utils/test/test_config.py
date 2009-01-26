# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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
