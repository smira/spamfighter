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
Базовые варианты тестовых сценариев на хранилища.
"""

from spamfighter.utils.time import startUpTestTimer, advanceTestTimer, tearDownTestTimer

class ExpirableStorageTestMixin():
    """
    Тест на L{spamfighter.interfaces.IExpirableStorage}.
    """

    def setUp(self):
        startUpTestTimer(1000)

    def tearDown(self):
        tearDownTestTimer()

    def testGetNotFound(self):
        return self.s.get('no').addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testGetOk(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.get('key')).addCallback(self.assertEquals, 'value')

    def testGetExpired(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: advanceTestTimer(1)).addCallback(lambda _: self.s.get('key')) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testAdd(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.add('key', 'value2', 1)).addCallback(lambda _: self.assert_(False)) \
                .addErrback(lambda failure: failure.trap(KeyError)).addCallback(lambda _: advanceTestTimer(1)) \
                .addCallback(lambda _: self.s.add('key', 'value2', 1)).addCallback(lambda _: self.s.get('key')) \
                .addCallback(self.assertEquals, 'value2')

    def testAppendNotFound(self):
        return self.s.append('no', '').addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testAppendTypeError1(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.append('key', 35)) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(TypeError))

    def testAppendTypeError2(self):
        return self.s.set('key', 35, 1).addCallback(lambda _: self.s.append('key', 'value')) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(TypeError))

    def testAppend(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.append('key', 'add')).addCallback(lambda _: self.s.get('key')) \
                .addCallback(self.assertEquals, 'valueadd')

    def testIncrNotFound(self):
        return self.s.incr('no', 2).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testIncrTypeError1(self):
        return self.s.set('key', 10, 1).addCallback(lambda _: self.s.incr('key', 'value')) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(TypeError))

    def testIncrTypeError2(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.incr('key', 1)) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(TypeError))

    def testIncr(self):
        return self.s.set('key', 5, 1).addCallback(lambda _: self.s.incr('key', 3)).addCallback(lambda _: self.s.get('key')) \
                .addCallback(self.assertEquals, 8)

    def testDeleteNotFound(self):
        return self.s.delete('no').addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testDelete(self):
        return self.s.set('key', 'value', 1).addCallback(lambda _: self.s.delete('key')).addCallback(lambda _: self.s.get('key')) \
                .addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap(KeyError))

    def testSetUnlimited(self):
        return self.s.set('key_u', 'value', 0).addCallback(lambda _: advanceTestTimer(1000000)).addCallback(lambda _: self.s.get('key_u')) \
                .addCallback(self.assertEquals, 'value')
