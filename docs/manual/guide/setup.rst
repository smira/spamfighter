.. SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. $Id$

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
