# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.info.version}.
"""

from twisted.trial import unittest

from spamfighter.api.info.version import InfoVersionCommand

class InfoVersionTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.info.version.InfoVersionCommand}.
    """

    def testRun(self):
        from spamfighter import version
        c = InfoVersionCommand()
        return c.run().addCallback(lambda _: self.assertEqual(version, c.result.version))
        
