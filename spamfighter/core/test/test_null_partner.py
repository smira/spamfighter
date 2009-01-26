# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
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
Тест на L{spamfighter.core.null_partner}.
"""

from twisted.trial import unittest

from zope.interface import verify as ziv

from spamfighter.interfaces import IPartner, IPartnerAuthorizer
from spamfighter.core.domain import BaseDomain, getDefaultDomain
from spamfighter.core.partner import PartnerAuthorizationFailedError
from spamfighter.core.null_partner import NullPartnerAuthorizer, NullPartner

class NullPartnerAuthorizerTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.null_partner.NullPartnerAuthorizer}.
    """

    def testInterface(self):
        ziv.verifyClass(IPartnerAuthorizer, NullPartnerAuthorizer)

    def testAuthorizeFailure(self):
        return NullPartnerAuthorizer().authorize({'login': 'a', 'password' : 'dddd'}).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(PartnerAuthorizationFailedError))

    def testAuthorizeOk(self):
        return NullPartnerAuthorizer().authorize(None).addCallback(lambda partner: self.assert_(isinstance(partner, NullPartner)))

class NullPartnerTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.null_partner.NullPartner}.
    """

    def testInterface(self):
        ziv.verifyClass(IPartner, NullPartner)

    def testRootDomain(self):
        def checkIt(rootDomain):
            self.assert_(isinstance(rootDomain, BaseDomain))
            self.assert_(rootDomain.parent() is getDefaultDomain())

        return NullPartner().rootDomain().addCallback(checkIt)

