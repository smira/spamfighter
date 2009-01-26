.. SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. $Id$

.. index::
   pair: разработка; установка

.. _dev-environment:

Подготовка окружения
====================

Кроме действий, описанных в разделе :ref:`user-setup`, необходимо дополнительно установить:

* qooxdoo 0.8 или trunk (http://qooxdoo.org/)
* Sphinx (http://sphinx.pocoo.org/)
* pydoctor (http://codespeak.net/~mwh/pydoctor/)

Установка Sphinx::

    easy_install Sphinx

Установка pydoctor описана на его странице: http://codespeak.net/~mwh/pydoctor/. Дополнительно к pydoctor
потребуется Divmod Nevow (http://divmod.org/trac/wiki/DivmodNevow), для python 2.5 достаточно сделать::

    easy_install Nevow

Для python 2.6 необходимо использовать версию из trunk::

    svn co http://divmod.org/svn/Divmod/trunk/Nevow/ Nevow
    cd Nevow
    python setup.py build
    sudo python setup.py install

Исходники СпамоБорца необходимо получить из репозитория::

    svn co svn://svn.netstream.ru/projects/antispam/trunk/ spamfighter

.. index:: unit-тест

Запуск unit-тестов
^^^^^^^^^^^^^^^^^^

Для запуска unit-тестов необходимо запустить скрипт run.tests.sh из корневого каталога СпамоБорца::

    ./run.tests.sh

При правильной настройке все тесты должны отрабатывать без ошибок.
