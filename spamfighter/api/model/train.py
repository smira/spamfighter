# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Команда C{sf.model.train} - обучение модели.
"""

import types
from zope.interface import implements

from spamfighter.core.commands import ICommand, install, errors
from spamfighter.core.model.command import ModelBaseCommand

class ModelTrainCommand(ModelBaseCommand):
    """
    Реализация команды C{sf.model.train}.
    """
    implements(ICommand)

    commandName = 'sf.model.train'
    commandSignature = {
            'marker' :          { 'type' : types.StringType, 'required' : True },
                       }
    resultSignature = {
                      }

    install()

    def perform(self):
        if self.params.marker not in ['good', 'bad']:
            raise errors.TypeParameterException, 'marker'

        return self.model.train(self.text, self.params.marker == 'good')

