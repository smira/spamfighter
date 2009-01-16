# -*- coding: utf-8 -*-
#
# SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Сообщения, атрибуты, их домены и т.п.
"""

from spamfighter.core.message.message import Message, TaggedMessage, MessageDomain
from spamfighter.core.message.attribute import UniqueIntAttributeDomain, TextAttributeDomain, AttributeNotFoundError, IPAttributeDomain
from spamfighter.core.message.serialize import ITransitMessage, TransitMessage
