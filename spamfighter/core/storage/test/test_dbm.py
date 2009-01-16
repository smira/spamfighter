# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.core.storage.dbm}.
"""

import os
import os.path
import shutil

from zope.interface import verify as ziv
from twisted.trial import unittest

from spamfighter.interfaces import IExpirableStorage, IPersistentStorage, IDomainBindable
from spamfighter.core.storage.dbm import DBMStorage, DomainedDBMStorage
from spamfighter.core.storage.test.base import ExpirableStorageTestMixin
from spamfighter.core.domain import getDefaultDomain
from spamfighter.utils import config

class DBMStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.dbm.DBMStorage}.
    """

    def setUp(self):
        if not os.path.exists(config.storage.dbm.path):
            os.makedirs(config.storage.dbm.path)
        ExpirableStorageTestMixin.setUp(self)
        self.s = DBMStorage('testing', 't')

    def tearDown(self):
        shutil.rmtree(config.storage.dbm.path)
        ExpirableStorageTestMixin.tearDown(self)

    def testInterface(self):
        ziv.verifyClass(IPersistentStorage, DBMStorage)
        ziv.verifyClass(IExpirableStorage,DBMStorage)

class DomainedDBMStorageTestCase(unittest.TestCase, ExpirableStorageTestMixin):
    """
    Тест на L{spamfighter.core.storage.dbm.DomainedDBMStorage}.
    """

    def setUp(self):
        if not os.path.exists(config.storage.dbm.path):
            os.makedirs(config.storage.dbm.path)
        ExpirableStorageTestMixin.setUp(self)
        self.s = DomainedDBMStorage()
        self.s.bind(getDefaultDomain(), 'testDBM')

    def tearDown(self):
        shutil.rmtree(config.storage.dbm.path)
        ExpirableStorageTestMixin.tearDown(self)

    def testInterface(self):
        ziv.verifyClass(IExpirableStorage, DomainedDBMStorage)
        ziv.verifyClass(IPersistentStorage, DomainedDBMStorage)
        ziv.verifyClass(IDomainBindable, DomainedDBMStorage)

    def testPickling(self):
        import pickle

        s2 = pickle.loads(pickle.dumps(self.s))
