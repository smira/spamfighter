# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# $Id$

"""
Тесты на L{spamfighter.api.message.input}.
"""

from twisted.trial import unittest

from spamfighter.api.message.input import MessageInputCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage

class MessageInputCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.input.MessageInputCommand}.
    """

    def testRun(self):
        c = MessageInputCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={ 'text' : u'Is this SPAM?'})
        return c.run().addCallback(lambda _: self.assertEqual('UNKNOWN', c.result.result))
        

