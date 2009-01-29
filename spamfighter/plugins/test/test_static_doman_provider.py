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

