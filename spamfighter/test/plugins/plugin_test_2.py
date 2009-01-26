# -*- coding: utf-8 -*-
#
# SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

from zope.interface import implements
from twisted.plugin import IPlugin

from spamfighter.test.plugins import ITestPlugin1, ITestPlugin2

class TestPlugin2(object):
    implements(IPlugin, ITestPlugin1, ITestPlugin2)

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

plugin1 = TestPlugin2('testplugin2')
plugin2 = TestPlugin2('testplugin3')
plugin3 = TestPlugin2('testplugin3')

