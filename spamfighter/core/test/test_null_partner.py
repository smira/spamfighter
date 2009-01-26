# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

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

