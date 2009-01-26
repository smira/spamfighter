# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Плагин для запуска СпамоБорца через twistd.
"""

from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.python import usage

from spamfighter import service

class SpamFighterServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "spamfighter"
    description = "A Spam Fighter web service"
    options = usage.Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """

        # Загружаем команды

        return service.makeService()

serviceMaker = SpamFighterServiceMaker()

