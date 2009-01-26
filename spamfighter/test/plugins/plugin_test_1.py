# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.test.plugins import ITestPlugin1

class TestPlugin1(object):
    implements(IPlugin, ITestPlugin1)

    def name(self):
        return 'testplugin1'

plugin1 = TestPlugin1()
