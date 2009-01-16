# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.model.classify} - классификация по модели.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, errors
from spamfighter.core.model.command import ModelBaseCommand

class ModelClassifyCommand(ModelBaseCommand):
    """
    Реализация команды C{sf.model.classify}.
    """
    implements(ICommand)

    commandName = 'sf.model.classify'
    commandSignature = {
                       }
    resultSignature = {
            'marker' :          { 'type' : types.StringType, 'required' : True },
                      }

    install()

    def perform(self):
        def gotResult(result):
            if result:
                self.result.marker = 'good'
            else:
                self.result.marker = 'bad'
        return self.model.classify(self.text).addCallback(gotResult)

