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
Тесты на L{spamfighter.api.domain.list}.
"""

from twisted.trial import unittest

from spamfighter.api.domain.list import DomainListCommand
from spamfighter.core.commands.partner import PartnerAuthInfo

class DomainListCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.domain.list.DomainListCommand}.
    """

    def testRun(self):
        c = DomainListCommand()
        c.params.partner = PartnerAuthInfo(None)
        return c.run().addCallback(lambda _: self.assertEqual(c.result.properties, []))

