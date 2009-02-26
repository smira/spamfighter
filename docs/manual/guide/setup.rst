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

Возможны несколько вариантов установки:

* с помощью средств ОС;
* из пакета Python с исходном кодом/бинарного пакета;
* из репозитория.

С помощью средств ОС
--------------------

В данный момент пакет СпамоБорца еще не включен ни в одну ОС.

Установка из пакета
-------------------

Предварительно необходимо установить `python <http://www.python.org/>`_ 2.5 или 2.6, а также 
`setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_. Обычно
эти пакеты уже установлены в ОС.

Установка из пакета выполняется просто::

  easy_install spamfighter

Данная команда автоматически обращается к `Python Package Index (PyPI) <http://pypi.python.org/>`_, находит последнюю
версию СпамоБорца, скачивает и устанавливает её. Также можно скачать пакет СпамоБорца
с сайта http://spam-fighter.ru/ и установить его с помощью easy_install (egg) или
просто распаковав архив (binary distribution). 

Еще одним способом установки является скачивание исходного пакета Python (source distribution) и 
установка вручную::

  python setup.py build
  python setup.py install

Далее см. :ref:`running`.

Установка из репозитория
------------------------

Установка из репозитория подробно описана в :ref:`руководстве разработчика <dev-environment>`.
