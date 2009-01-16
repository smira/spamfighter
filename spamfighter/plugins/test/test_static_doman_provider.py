# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.plugins.static_domain_provider}.
"""

import unittest

from zope.interface import verify as ziv
from twisted.plugin import IPlugin

from spamfighter.interfaces import IDomain
from spamfighter.plugin import IDefaultDomainProvider
from spamfighter.plugins.static_domain_provider import emptyDomainProvider, StaticDefaultDomainProvider

class StaticDefaultDomainProviderTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugins.static_domain_provider.StaticDefaultDomainProvider}.
    """

    def testInterface(self):
        ziv.verifyClass(IPlugin, StaticDefaultDomainProvider)
        ziv.verifyClass(IDefaultDomainProvider, StaticDefaultDomainProvider)

    def testEmptyDomain(self):
        domain = emptyDomainProvider.getDefaultDomain()
        ziv.verifyObject(IDomain, domain)

