# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.domain.list}.
"""

from twisted.trial import unittest

from spamfighter.api.domain.list import DomainListCommand
from spamfighter.core.commands.partner import PartnerAuthInfo

class DomainListCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.domain.list.DomainListCommand}.
    """

    def testRun(self):
        c = DomainListCommand()
        c.params.partner = PartnerAuthInfo(None)
        return c.run().addCallback(lambda _: self.assertEqual(c.result.properties, []))

