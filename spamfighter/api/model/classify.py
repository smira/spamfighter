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

