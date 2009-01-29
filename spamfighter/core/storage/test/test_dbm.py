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
