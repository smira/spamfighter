.. SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. $Id$

Работа с документацией
======================

Данная документация генерируется из исходных файлов в формате ReST с помощью Sphinx (http://sphinx.pocoo.org/). Для
создания HTML-документации::

    make manual

Готовая документация будет размещена в каталоге::

    docs/manual/.build/html/

Документация по исходному коду генерируется с помощью pydoctor (http://codespeak.net/~mwh/pydoctor/), для генерации
необходимо из корневого каталога исходного кода::

    make source-docs

Документация по исходному коду будет сгенерирована в каталоге::

    docs/api/

Подробнее об установке pydoctor и Sphinx см. раздел :ref:`dev-environment`.
