.. SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. This file is part of SpamFighter.
.. 
.. SpamFighter is free software: you can redistribute it and/or modify
.. it under the terms of the GNU General Public License as published by
.. the Free Software Foundation, either version 3 of the License, or
.. (at your option) any later version.
.. 
.. SpamFighter is distributed in the hope that it will be useful,
.. but WITHOUT ANY WARRANTY; without even the implied warranty of
.. MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
.. GNU General Public License for more details.
.. 
.. You should have received a copy of the GNU General Public License
.. along with SpamFighter.  If not, see <http://www.gnu.org/licenses/>.
.. 

.. index::
   pair: установка; запуск

.. _user-setup:

Установка СпамоБорца
====================

Для установки потребуются:

* python 2.5 или 2.6 (http://www.python.org/)
* Twisted Framework 8.0+ (http://twistedmatrix.com/)
* pyparsing (http://pyparsing.wikispaces.com/)
* simplejson (для python 2.5) (http://code.google.com/p/simplejson/)
* pyOpenSSL (http://pyopenssl.sourceforge.net/)

После установки python все модули можно поставить с помощью программы easy_install или другого
механизма, специфичного для конкретной ОС::

  easy_install Twisted
  easy_install pyparsing
  easy_install simplejson (для python2.5)
  easy_install pyOpenSSL
  easy_install netaddr

Если планируется использовать HTTPS (а он включен в СпамоБорце по умолчанию), необходимо сгенерировать
сертификаты сервера. Для этого необходимо::

  make https-cert

Установка на Gentoo Linux
-------------------------

.. code-block:: sh

  emerge dev-python/twisted dev-python/twisted-conch dev-python/twisted-web
  emerge simplejson
  easy_install pyparsing
  easy_install netaddr

Pyparsing в Portage слишком старой версии, поэтому приходится его ставить через easy_install,
netaddr же отсутствует в Portage.
