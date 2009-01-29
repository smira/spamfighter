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

