# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.partner}.
"""

from twisted.trial import unittest

from spamfighter.interfaces import IPartnerAuthorizer
from spamfighter.core.partner import getPartnerAuthorizer

class PartnerAuthorizerTestCase(unittest.TestCase):
    """
    Тест на предоставление механизма авторизации по умолчанию.
    """

    def testDefaultPartnerAuthorizer(self):
        authorizer = getPartnerAuthorizer()

        self.assert_(IPartnerAuthorizer.providedBy(authorizer))

    def testPartnerAuthorizer(self):
        self.assert_(getPartnerAuthorizer() is getPartnerAuthorizer())

