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
   pair: API; транспорт
   pair: API; JSON-RPC
   pair: API; XML-RPC

Транспорт API
=============

API СпамоБорца представляет собой набор команд, которые доступны через XML-RPC [#XML-RPC]_ и JSON-RPC [#JSON-RPC]_. В зависимости от настроек
сервера, они доступны через протоколы HTTP и HTTPS.

По умолчанию, JSON-RPC over HTTP доступен через URL: http://localhost:8000/api/json/, а XML-RPC: http://localhost:8000/api/xml/.

В обоих вариантах представления API используются следующие соглашения:

* имя команды API передается в качестве имени метода;
* любой вызов содержит ровно один позиционный RPC-параметр, который имеет тип "хэш", в этом параметре задаются все именованные
  параметры команды (некоторые из которых могут быть необязательными);
* результатом выполнения команды является хэш, который содержит параметры возврата.

Такая организация вызовов позволяет расширять команды новыми, необязательными параметрами в будущем.

Например, для вызова команды **sf.test** с параметром **a** со значением ``1`` и параметром **b** со значением ``"abcd"`` мы формируем следующий
вызов метода::

    sf.test({ a: 1, b : "abcd"})

Данный вызов будет закодирован следующим образом для XML-RPC:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <methodCall>
      <methodName>sf.test</methodName>
      <params>
        <param>
          <value>
            <struct>
              <member>
                <name>a</name>
                <value>
                  <i4>1</i4>
                </value>
              </member>
              <member>
                <name>b</name>
                <value>
                  <string>abcd</string>
                </value>
              </member>
            </struct>
          </value>
        </param>
      </params>
    </methodCall>

А для JSON-RPC так:

.. code-block:: javascript
   
   {
        "service":null,
        "method":"sf.test",
        "id":11,
        "params":
            [
                {
                    "a":1,
                    "b":"abcd"
                }
            ]
   }

Ответом сервера всегда является хэш, пусть нам должны вернуть параметр **d** со значением ``458``::

    { d : 458 }

Такой ответ в случае XML-RPC будет выглядеть следующим образом:


.. code-block:: xml

    <?xml version="1.0"?>
    <methodResponse>
      <params>
        <param>
          <value>
            <struct>
              <member>
                <name>d</name>
                <value>
                  <i4>458</i4>
                </value>
              </member>
            </struct>
          </value>
        </param>
      </params>
    </methodResponse>

А для JSON-RPC случая так:

.. code-block:: javascript

   {"result": {"d": 458}, "id": 11}

Для доступа к API можно использовать существующие библиотеки XML-RPC или JSON-RPC, а также :ref:`клиенты <api-clients>`, входящие в поставку СпамоБорца.

.. [#JSON-RPC]              http://json-rpc.org/
.. [#XML-RPC]               http://en.wikipedia.org/wiki/XML-RPC/
