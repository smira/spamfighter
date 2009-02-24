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

.. _dev-make:

Директивы Makefile
==================

В корне исходного кода СпамоБорца расположен Makefile, который позволяет получить быстрый доступ
к различным ежедневным операциям.

``all`` или ``unittest``
    Или аргумент по умолчанию, просто "make" - запустить юнит-тесты СпамоБорца. Юнит-тесты запускаются
    с помощью trial, подсистемы юнит-тестов Twisted Framework.

``docs``
    Построить документацию (это руководство) и документацию по исходному коду. Включает цели ``manual`` и ``apidocs``.

``clean``
    Очистить все ранее собранные элементы.

``dist``
    Собрать исходный и бинарные пакеты СпамоБорца.

``debug-jsadmin``
    Собрать отладочный вариант системы управления СпамоБорцем (qooxdoo).
