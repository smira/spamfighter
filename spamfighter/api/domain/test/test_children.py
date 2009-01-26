# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.domain.children}.
"""

from twisted.trial import unittest

from spamfighter.api.domain.children import DomainChildrenCommand
from spamfighter.core.commands.partner import PartnerAuthInfo

class DomainChildrenCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.domain.children.DomainChildrenCommand}.
    """

    def testRun(self):
        c = DomainChildrenCommand()
        c.params.partner = PartnerAuthInfo(None)
        return c.run().addCallback(lambda _: self.assertEqual(c.result.children, []))

