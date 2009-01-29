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
Тесты на L{spamfighter.core.domain}.
"""

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IDomain
from spamfighter.core.domain import BaseDomain, DomainKeyError, getDefaultDomain, \
        DomainDuplicateError, DomainPathError


class BaseDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.domain.BaseDomain}.
    """

    def testInterface(self):
        ziv.verifyClass(IDomain, BaseDomain)

    def testParent(self):
        domain1 = BaseDomain(key='d')
        domain2 = BaseDomain(parent=domain1, name='sub2')

        self.assertEqual(None, domain1.parent())
        self.assertEqual(domain1, domain2.parent())

    def testKey(self):
        self.assertEqual('testKey', BaseDomain(key='testKey').key())

        domain1 = BaseDomain(key='testKey')
        domain2 = BaseDomain(parent=domain1, key='testKey2')
        self.assertEqual('testKey2', domain2.key())
        domain3 = BaseDomain(parent=domain1, name='sub3')
        self.assertEqual('676c7a29cea4e68de9e65b331ea275fb', domain3.key())

    def testName(self):
        self.assertEqual(None, BaseDomain(key='d').name())
        self.assertEqual('chat', BaseDomain(key='d2', name='chat').name())

    def testChildren(self):
        return BaseDomain(key='d').children().addCallback(self.assertEqual, dict())

    def testCreateSubdomain(self):
        domain = BaseDomain(key='d')

        def checkIt(child):
            def checkChildren(children):
                self.assertEquals(['sub'], children.keys())
                self.assert_(child is children['sub'])

            return domain.children().addCallback(checkChildren)

        return domain.createSubdomain('sub').addCallback(checkIt)

    def testCreateSubdomainDuplicate(self):
        domain = BaseDomain(key='d')
        return domain.createSubdomain('sub').addCallback(lambda _: domain.createSubdomain('sub')) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(DomainDuplicateError))
    
    def testWalk(self):
        domain = BaseDomain(key='d')

        def gotChild1(d):
            child1 = d

            def gotChild2(d):
                child2 = d

                def gotSubchild1(d):
                    subchild1 = d

                    return domain.walk('').addCallback(lambda result: result is domain) \
                            .addCallback(lambda _: domain.walk('///')).addCallback(lambda result: self.assert_(result is domain)) \
                            .addCallback(lambda _: domain.walk('/child1/')).addCallback(lambda result: self.assert_(result is child1)) \
                            .addCallback(lambda _: domain.walk('child1')).addCallback(lambda result: self.assert_(result is child1)) \
                            .addCallback(lambda _: domain.walk('child2')).addCallback(lambda result: self.assert_(result is child2)) \
                            .addCallback(lambda _: domain.walk('child1/sub1')).addCallback(lambda result: self.assert_(result is subchild1)) \
                            .addCallback(lambda _: domain.walk('unknown')).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(DomainPathError)) \
                            .addCallback(lambda _: domain.walk('child1/unknown')).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(DomainPathError)) \
                            .addCallback(lambda _: domain.walk('child1/sub1/unknown')).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(DomainPathError)) 

                return child1.createSubdomain('sub1').addCallback(gotSubchild1)
            return domain.createSubdomain('child2').addCallback(gotChild2)
        return domain.createSubdomain('child1').addCallback(gotChild1)

    def testGet(self):
        domain = BaseDomain(dict={'a' : 33}, key='d')

        self.assertEqual(33, domain.get('a'))
        self.assertRaises(DomainKeyError, domain.get, 'b')

        domain2 = BaseDomain(parent=domain, dict={'c' : 44}, name='sub')
        self.assertEqual(33, domain2.get('a'))
        self.assertEqual(44, domain2.get('c'))
        self.assertRaises(DomainKeyError, domain2.get, 'b')

    def testHas(self):
        domain = BaseDomain(dict={'a' : 33}, key='d')

        self.assertEqual(True, domain.has('a'))
        self.assertEqual(False, domain.has('b'))

    def testSet(self):
        domain = BaseDomain(key='d')
        return domain.set('fff', 'ggg').addCallback(lambda _: self.assertEqual('ggg', domain.get('fff')))

    def testDelete(self):
        domain = BaseDomain(dict={'lll':'dsd'}, key='d')
        return domain.delete('lll').addCallback(lambda _: self.assertRaises(DomainKeyError, domain.get, 'lll')) \
                .addCallback(lambda _: domain.delete('lll'))

    def testList(self):
        domain = BaseDomain(dict={'a' : 33, 'b' : 44}, key='d')
        self.assertEqual(['a', 'b'], domain.list())

        domain = BaseDomain(dict={}, key='d')
        self.assertEqual([], domain.list())

class DefaultDomainTestCase(unittest.TestCase):
    """
    Тест на предоставление домена по умолчанию.
    """

    def testDefaultDomain(self):
        domain = getDefaultDomain()

        self.assert_(IDomain.providedBy(domain))
        self.assertEqual(None, domain.parent())
        # у домена по умолчанию не может быть явных детей, т.к. он не допускает итерацию
        return domain.children().addCallback(self.assertEqual, {})

