# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Базовые классы для обработки команд API сервера.
"""

from spamfighter.core.commands.command import ICommand, Command, Array
from spamfighter.core.commands.serialize import ISerializable
from spamfighter.core.commands.dispatcher import install, dispatchCommand
from spamfighter.core.commands.partner import PartneredCommand, DomainedCommand
