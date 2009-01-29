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
Плагин, реализующий корневой домен в качестве возможного примера организации.
"""

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.plugin import IDefaultDomainProvider

class SampleDomainProvider(object):
    """
    Провайдер статического дефолтного домена.
    """
    implements(IPlugin, IDefaultDomainProvider)

    def __init__(self):
        """
        Конструктор.
        """

    def name(self):
        """
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return 'SampleDomainProvider'

    def getDefaultDomain(self):
        """
        Получить домен по умолчанию в системе.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IDomain}
        """
        from spamfighter.core.domain import BaseDomain, getDefaultDomain
        from spamfighter.core.firewall import MessageFirewall
        from spamfighter.core.model.bayes import BayesModel
        from spamfighter.core.message import MessageDomain, TextAttributeDomain, UniqueIntAttributeDomain, IPAttributeDomain
        from spamfighter.core.storage.memory import DomainMemoryStorage
        from spamfighter.core.storage.dbm import DomainedDBMStorage
        from spamfighter.core.log import MessageLog
        from spamfighter.core.counters import RequestPerSecondCounter, RequestCounter, AverageServiceTimeCounter

        domain = BaseDomain(parent=getDefaultDomain(), key='sample_root')

        rules = """
do lengthCheck(minLength=1, maxLength=1000) mark invalid
do regexpCheck(regexp="[a-z]+") mark notalpha
if invalid, notalpha skip to 1000
do messageFloodCheck() mark flood
do messageFrequencyCheck() mark messagefrequent, frequent
do userFrequencyCheck() mark userfrequent, frequent
if frequent skip to 1000
do modelClassify(model="model2") mark spam
do messageLogPut(log="messageLog2")
1000: do messageLogPut()
if invalid stop as INVALID
if frequent stop as FREQUENT
if spam stop as SPAM
stop as OK
        """.strip()
 
        domain.set('model', BayesModel())
        domain.set('model2', BayesModel())
        domain.set('messageAnalyzer', MessageFirewall(rules))
        domain.set('storage', DomainMemoryStorage())
        domain.set('logStorage', DomainMemoryStorage())
        domain.set('db', DomainedDBMStorage())
        domain.set('messageLog', MessageLog(storage='logStorage'))
        domain.set('messageLog2', MessageLog(storage='logStorage'))

        domain.set('counterRequest', RequestCounter())
        domain.set('counterRPS', RequestPerSecondCounter())
        domain.set('counterAST', AverageServiceTimeCounter())

        def fillS1(subdomain_1):
            subdomain_1.set('model2', BayesModel())
            subdomain_1.set('counterRequest', RequestCounter())
            subdomain_1.set('counterRPS', RequestPerSecondCounter())
            subdomain_1.set('counterAST', AverageServiceTimeCounter())

            def fillS1_1(subdomain_1_1):
                subdomain_1_1.set('messageLog', MessageLog(storage='logStorage'))

            subdomain_1.createSubdomain('s1_1').addCallback(fillS1_1)

        domain.createSubdomain('s1').addCallback(fillS1)

        domain.createSubdomain('s2')

        return domain

sampleDomainProvider = SampleDomainProvider()

