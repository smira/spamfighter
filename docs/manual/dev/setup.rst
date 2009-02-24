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
   pair: разработка; установка

.. _dev-environment:

Установка и подготовка
======================

Установка
---------

Для запуска и работы со СпамоБорцем потребуются:

* python 2.5 или 2.6 (http://www.python.org/)
* Twisted Framework 8.0+ (http://twistedmatrix.com/)
* pyparsing (http://pyparsing.wikispaces.com/)
* simplejson (для python 2.5) (http://code.google.com/p/simplejson/)
* pyOpenSSL (http://pyopenssl.sourceforge.net/)
* qooxdoo 0.8 или trunk (http://qooxdoo.org/)
* Sphinx (http://sphinx.pocoo.org/)
* pydoctor (http://codespeak.net/~mwh/pydoctor/)

После установки python все модули можно поставить с помощью программы easy_install или другого
механизма, специфичного для конкретной ОС::

  easy_install Twisted
  easy_install pyparsing
  easy_install simplejson (для python2.5)
  easy_install pyOpenSSL
  easy_install netaddr

Установка Sphinx::

    easy_install Sphinx

Установка pydoctor описана на `его странице <http://codespeak.net/~mwh/pydoctor/>`_. Дополнительно к pydoctor
потребуется `Divmod Nevow <http://divmod.org/trac/wiki/DivmodNevow>`_, для python 2.5 достаточно сделать::

    easy_install Nevow

Для python 2.6 необходимо использовать версию из trunk::

    svn co http://divmod.org/svn/Divmod/trunk/Nevow/ Nevow
    cd Nevow
    python setup.py build
    sudo python setup.py install


Исходники СпамоБорца необходимо получить из репозитория::

    git clone http://spam-fighter.ru/git/ spamfighter.git

После скачивания qooxdoo SDK необходимо сделать symlink c каталога, куда был распакован архив, в каталог `admin/qooxdoo`::

    ln -s /var/qooxdoo-0.8-sdk spamfighter.git/admin/qooxdoo


Запуск unit-тестов
------------------

Для запуска unit-тестов из корневого каталога СпамоБорца::

    make

При правильной настройке все тесты должны отрабатывать без ошибок.

Создание документации
---------------------

Для создания руководства из исходников с помощью Sphinx::

  make manual

Построение документации по исходному коду с помощью pydoctor::
  
  make apidocs

Построение системы управления на qooxdoo
----------------------------------------

Отладочный вариант системы управления::

  make debug-jsadmin

Другие параметры Makefile см. в :ref:`специальном разделе <dev-make>`.

Запуск сервера
--------------

Находясь в корневом каталоге СпамоБорца можно запустить его, выполнив::

  twistd -n spamfighter
