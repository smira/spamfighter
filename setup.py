#!/usr/bin/env python
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

from distutils.core import setup
import os
import fnmatch

def build_datafiles(source_root, destination_root):
    result = []
    ignores = [line.strip() for line in open('.gitignore', 'r').readlines()]
    for root, dirs, files in os.walk(source_root):
        filtered_files = filter(lambda file: not any(map(lambda pattern: fnmatch.fnmatch(file, pattern), ignores)), files)
        result.append((os.path.join(destination_root, os.path.relpath(root, source_root)), 
                [os.path.join(root, file) for file in filtered_files]))

    return result

setup(name='spamfighter',
      version='0.1.0',
      description='Web-service fighting spam and other unsolicited messages',
      author='Andrey Smirnov',
      author_email='me@smira.ru',
      url='http://spam-fighter.ru/',
      data_files = build_datafiles('admin/build/', 'share/spamfighter/admin') + \
              build_datafiles('docs/manual/.build/html/', 'share/spamfighter/manual') + \
              build_datafiles('html/', 'share/spamfighter/public_html') + 
              build_datafiles('docs/api/', 'share/spamfighter/apidocs') + 
              [('share/spamfighter/cert/scripts', ['cert/scripts/generateLocal.sh', 'cert/scripts/openssl.cnf'])],
      license='GPLv3',
      long_description="""SpamFighter combines several methods for filtering spam and other unsolicited messages (comments, chat etc.):
 - rule-based filtering
 - trained models
 - black-lists
 - frequency checking
 - and many more.

SpamFighter provides XML- and JSON-RPC API for incoming message filtering and configuration requests. It comes with
lightweight browser-based configuration tool, examples, plugin architecture and much more.
""",
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Environment :: No Input/Output (Daemon)',
            'Framework :: Twisted',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: Russian',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: BSD',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.5',
            'Topic :: Security',
            'Topic :: Communications',
          ],
      packages=['spamfighter', 
          'spamfighter.api',
            'spamfighter.api.domain', 'spamfighter.api.domain.test',
            'spamfighter.api.info', 'spamfighter.api.info.test',
            'spamfighter.api.message', 'spamfighter.api.message.test',
            'spamfighter.api.model', 'spamfighter.api.model.test',
          'spamfighter.core',
            'spamfighter.core.commands', 'spamfighter.core.commands.test',
            'spamfighter.core.message', 'spamfighter.core.message.test',
            'spamfighter.core.model', 'spamfighter.core.model.test',
            'spamfighter.core.storage', 'spamfighter.core.storage.test',
            'spamfighter.test',
          'spamfighter.plugins', 
            'spamfighter.plugins.test',
          'spamfighter.rules', 
            'spamfighter.rules.test',
          'spamfighter.test',
            'spamfighter.test.plugins',
          'spamfighter.utils', 
            'spamfighter.utils.test',
          'spamfighter.txjsonrpc',
            'spamfighter.txjsonrpc.web', 'spamfighter.txjsonrpc.web.test',
            'spamfighter.txjsonrpc.test',
	  'twisted.plugins',
            ],
     )

