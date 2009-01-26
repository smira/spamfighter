# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.plugins.null_partner_authorizer_provider}.
"""

import unittest

from zope.interface import verify as ziv
from twisted.plugin import IPlugin

from spamfighter.interfaces import IPartnerAuthorizer
from spamfighter.plugin import IPartnerAuthorizerProvider
from spamfighter.plugins.null_partner_authorizer_provider import nullPartnerAuthorizer, NullPartnerAuthorizerProvider

class NullPartnerAuthorizerProviderTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugins.null_partner_authorizer_provider.NullPartnerAuthorizerProvider}.
    """

    def testInterface(self):
        ziv.verifyClass(IPlugin, NullPartnerAuthorizerProvider)
        ziv.verifyClass(IPartnerAuthorizerProvider, NullPartnerAuthorizerProvider)

    def testGetAuthorizer(self):
        authorizer = nullPartnerAuthorizer.getPartnerAuthorizer()
        ziv.verifyObject(IPartnerAuthorizer, authorizer)

