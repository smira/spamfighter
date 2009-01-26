.. SpamFigher, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. $Id$

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
