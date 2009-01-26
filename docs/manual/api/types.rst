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
   pair: API; типы данных

Типы данных
===========

.. index::
   pair: API; партнер

.. _api-partner:

Partner
-------

Информация о партнере, относительно которого должна выполняться данная команда.
Партнер авторизует вызов API.

Информация, передаваемая в этом параметре, зависит от текущего :ref:`механизма авторизации партнеров <authorize-provider>`,
для :ref:`доверительного механизма авторизации <null-partner-authorizer>` это всегда ``null`` (или ``None``, ``nil``, в зависимости
от языка программирования и способа сериализации).

.. index::
   pair: API; домен

.. _api-domain:

Domain
------

Путь к домену, относительного которого будет происходить выполнение команды. Путь задается
относительного корневого :ref:`домена <domain>` текущего :ref:`партнера <partner>`. 

Если параметр не задан, равен ``""`` или ``"/"``, команда исполняется относительного корневого
домена партнера. Если параметр равен, например, ``"a/b"``, команда исполняется в поддомене ``b``
поддомена ``a`` корневого домена текущего партнера.

.. index::
   pair: API; сообщение

.. _api-message:

Message
-------

Сериализованное представление :ref:`сообщения <message>` при передаче в :ref:`api`. Данный тип 
данных - это хэш, ключами которого являются имена :ref:`атрибутов <message-attribute>` сообщения,
а значениями - значения этих атрибутов, сериализованные относительно соответствующих 
:ref:`доменов атрибутов <attribute-domain>`. Десериализация сообщения выполняется всегда
относительного выбранного :ref:`домена <domain>`, при этом осуществляется поиск по имени
домена атрибута в :ref:`домене сообщения <message-domain>` и десериализация в соответствующий
атрибут сообщения.

Например, пусть в параметре ``messageDomain`` текущего домена хранится такой домен сообщения:

.. code-block:: python

   MessageDomain(TextAttributeDomain("text"), UniqueIntAttributeDomain("from"))

Тогда относительно данного домена будут валидными следующие сериализованные сообщения:

.. code-block:: javascript

   { }
   { 'text' : 'Is this SPAM?' }
   { 'text' : 'It is beatiful!', 'from' : 137 }

А следующие сериализованные сообщения не будут валидны:

.. code-block:: javascript

   { 'ip' : '127.0.0.1' }         /* неизвестный атрибут 'ip' */
   { 'from' : '127' }             /* неверный тип данных для атрибута 'from' */

.. _api-logentry:

LogEntry
--------

Отдельная запись в :ref:`логе сообщений <message-log>`, сериализованная для передачи через :ref:`api`. 
Данный тип данных представляет собой хэш с следующими ключами:

.. describe:: id

   ``integer`` ID записи в логе сообщений (уникально относительно лога сообщений)

.. describe:: when
   
   ``integer`` дата и время попадания записи в лог, время в секундах с 1 января 1970 г., UTC

.. describe:: tags

   ``Array(string)`` список тэгов, сохраненных в логе вместе с сообщением

.. describe:: message

   :ref:`Message <api-message>` сохраненное в логе сообщение

