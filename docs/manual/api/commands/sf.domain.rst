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

Команды управления доменами
===========================

.. index::
   pair: sf.domain.list; команда
   pair: sf.domain.list; домен

Команда sf.domain.list
----------------------

Получить список свойств :ref:`домена <domain>`.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, свойства которого мы хотим получить (*необязательный*)

Результат
^^^^^^^^^

.. describe:: propreties

    ``Array(string)`` список имен свойств домена

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
  
   {"service":null,"method":"sf.domain.children","id":4,"params":[{"partner":null,"domain":"comment"}]}

.. code-block:: javascript

   {"result": {"properties": ["storage", "model", "messageAnalyzer", "messageLog"]}, "id": 4}

.. index::
   pair: sf.domain.get; команда
   pair: sf.domain.get; домен

Команда sf.domain.get
----------------------

Получить подробную информацию о свойстве :ref:`домена <domain>`.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, свойства которого мы хотим получить (*необязательный*)

.. describe:: name

   ``string`` имя свойства домена

Результат
^^^^^^^^^

.. describe:: repr

    ``string`` некоторое строковое представление свойства домена

.. describe:: interfaces

    ``Array(string)`` список интерфейсов, которые поддерживает свойство домена

.. describe:: classname

    ``string`` класс (тип) свойства домена

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
 
   {"service":null,"method":"sf.domain.get","id":7,"params":[{"partner":null,"name":"storage"}]}

.. code-block:: javascript

   {
    "result": 
        {
            "classname": "DomainMemoryStorage", 
            "interfaces": ["IExpirableStorage", "IUnreliableStorage", "IDomainBindable"], 
            "repr": "<spamfighter.core.storage.memory.DomainMemoryStorage object at 0x2cd0cd0>"
         }, 
    "id": 7
   }


.. index::
   pair: sf.domain.children; команда
   pair: sf.domain.children; домен

Команда sf.domain.children
--------------------------

Получить список имен поддоменов указанного :ref:`домена <domain>`.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, свойства которого мы хотим получить (*необязательный*)

Результат
^^^^^^^^^

.. describe:: children

    ``Array(string)`` список имен поддоменов укзанного домена

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript

   {"service":null,"method":"sf.domain.children","id":2,"params":[{"partner":null}]}

.. code-block:: javascript

   {"result": {"children": ["comment", "chat", "pm"]}, "id": 2}
