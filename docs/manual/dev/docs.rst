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

Документация по исходному JavaScript-коду генерируется с помощью qooxdoo::

   cd admin/ && ./generate.py api
