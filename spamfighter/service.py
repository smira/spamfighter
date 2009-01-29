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
Построение сервисов, составляющих ядро сервера.
"""

import sys

from twisted.application import internet, service
from twisted.internet import protocol
from twisted.python import log

from spamfighter.utils import config

def makeService():
    """
    Построить главный сервис.
    Дочерними к нему будут основные сервисы СпамоБорца.

    @return: главный сервис
    """

    observer = log.FileLogObserver(sys.stderr)
    log.addObserver(observer.emit)

    from spamfighter import version
    log.msg("SpamFighter starting up (version %s)..." % version)

    s = service.MultiService()

    if config.http.enabled == "yes" or config.https.enabled == "yes":
        log.msg("> Starting HTTP services:")

        from twisted.web import server, resource, static

        root = resource.Resource()

        log.msg(">> Static HTTP @ /")
        static.File.contentTypes.update({'.html' : 'text/html; charset=utf-8'})
        root.putChild('', static.File('html/index.html'))
        root.putChild('favicon.ico', static.File('html/favicon.ico'))

        if config.manage.interface.enabled == "yes":
            log.msg(">>> Management interface @ /%s/" % config.manage.interface.location)
            root.putChild(config.manage.interface.location, static.File(config.manage.interface.path))

        if config.manage.js_api.enabled == "yes":
            log.msg(">>> JavaScript management API doc @ /%s/" % config.manage.js_api.location)
            root.putChild(config.manage.js_api.location, static.File(config.manage.js_api.path))

        if config.manage.debug.enabled == "yes":
            log.msg(">>> DEBUG: Management interface @ /%s/" % config.manage.debug.location)
            root.putChild(config.manage.debug.location, static.File(config.manage.debug.path))

        if config.docs.manual.enabled == "yes":
            log.msg(">>> Manual @ /%s/" % config.docs.manual.location)
            root.putChild(config.docs.manual.location, static.File(config.docs.manual.path))

        if config.docs.source.enabled == "yes":
            log.msg(">>> DEBUG: Source-docs @ /%s/" % config.docs.source.location)
            root.putChild(config.docs.source.location, static.File(config.docs.source.path))

        api = resource.Resource()
        root.putChild('api', api)

        if config.api.xmlrpc.enabled == "yes":
            log.msg(">> XML-RPC API @ /api/xml/")
            from spamfighter.core.commands.apiglue import XMLRPC_API_Glue

            api.putChild('xml', XMLRPC_API_Glue())
        if config.api.jsonrpc.enabled == "yes":
            log.msg(">> JSON-RPC API @ /api/json/")
            from spamfighter.core.commands.apiglue import JSONRPC_API_Glue

            api.putChild('json', JSONRPC_API_Glue())

        if config.http.enabled == "yes":
            log.msg(">> HTTP server (port %d)" % config.http.port)
            h = internet.TCPServer(config.http.port, server.Site(root))
            h.setServiceParent(s)

        if config.https.enabled == "yes":
            log.msg(">> HTTPS server (port %d)" % config.https.port)
            from twisted.internet import ssl

            h = internet.SSLServer(config.https.port, server.Site(root), ssl.DefaultOpenSSLContextFactory(
                    config.https.cert.private_key_file, config.https.cert.certificate_file))
            h.setServiceParent(s)

    if config.manhole.enabled == "yes":
        log.msg("> DEBUG: Starting manhole (port %d)" % config.manhole.port)
        log.msg("> DEBUG: Use 'telnet localhost %d' to login" % config.manhole.port)
        from twisted.conch.telnet import TelnetTransport, TelnetBootstrapProtocol
        from twisted.conch.insults import insults
        from twisted.conch.manhole import ColoredManhole

        f = protocol.ServerFactory()
        f.protocol = lambda: TelnetTransport(TelnetBootstrapProtocol,
                                             insults.ServerProtocol,
                                             ColoredManhole,
                                             None,
                                             )
        h = internet.TCPServer(config.manhole.port, f)
        h.setServiceParent(s)

    log.msg("Loading commands...")
    from spamfighter.api import loadCommands
    loadCommands()
    
    from spamfighter.core.commands.dispatcher import listAllCommands
    commandsList = listAllCommands()
    commandsList.sort()
    log.msg("Commands loaded: %s." % ', '.join(commandsList))

    log.msg("Loading rules...")
    from spamfighter.rules import loadRules
    loadRules()

    from spamfighter.core.rules import factory
    rulesList = factory.getRuleNames()
    rulesList.sort();
    log.msg("Rules loaded: %s." % ', '.join(rulesList))

    from spamfighter.core.domain import getDefaultDomain
    log.msg("Default domain: %r" % getDefaultDomain())

    from spamfighter.core.partner import getPartnerAuthorizer
    log.msg("Partner authorizer: %r" % getPartnerAuthorizer())

    log.msg("SpamFighter startup done.")
    log.removeObserver(observer.emit)

    return s
