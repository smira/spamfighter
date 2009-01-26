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

Информационные команды
======================

.. index::
   pair: sf.info.version; команда 

Команда sf.info.version
-----------------------

Получить версию сервера.

Авторизация
^^^^^^^^^^^

Не требуется.

Параметры
^^^^^^^^^

Нет.

Результат
^^^^^^^^^

.. describe:: version

    `string` версия сервера

Пример
^^^^^^

XML-RPC
"""""""

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <methodCall>
      <methodName>sf.info.version</methodName>
      <params>
        <param>
          <value>
            <struct/>
          </value>
        </param>
      </params>
    </methodCall>

.. code-block:: xml

    <?xml version="1.0"?>
    <methodResponse>
      <params>
        <param>
          <value>
            <struct>
              <member>
                <name>version</name>
                <value>
                  <string>0.1</string>
                </value>
              </member>
            </struct>
          </value>
        </param>
      </params>
    </methodResponse>

JSON-RPC
""""""""

.. code-block:: javascript

    {"service":null,"method":"sf.info.version","id":1,"params":[{}]}


.. code-block:: javascript

    {"result": {"version": "0.1"}, "id": 1}
