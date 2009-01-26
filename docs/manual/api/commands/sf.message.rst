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

Команды работы с сообщениями
============================

.. index::
   pair: sf.message.input; команда
   pair: sf.message.input; сообщение

.. _sf.message.input:

Команда sf.message.input
------------------------

Основная команда API СпамоБорца. Отправить :ref:`сообщение <message>` на обработку и получить результат классификации
сообщения.

Сообщение на сервере проходит через :ref:`firewall <firewall>`, результат анализа является результатом выполнения
команды.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, относительно которого проводить анализ (*необязательный*)

.. describe:: message

   :ref:`Message <api-message>` анализируемое сообщение

.. describe:: debug
   ``boolean`` включить отладочный режим (*необязательный*)

Результат
^^^^^^^^^

.. describe:: result

    ``string`` результат анализа

.. describe:: log
    
     ``string`` лог прохождения сообщения через firewall, только если был включен отладочный режим (*необязательный*)

Пример
^^^^^^

XML-RPC
"""""""

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <methodCall>
      <methodName>sf.message.input</methodName>
      <params>
        <param>
          <value>
            <struct>
              <member>
                <name>partner</name>
                <value>
                  <nil/>
                </value>
              </member>
              <member>
                <name>message</name>
                <value>
                  <struct>
                    <member>
                      <name>text</name>
                      <value>
                        <string>Is this message SPAM?</string>
                      </value>
                    </member>
                  </struct>
                </value>
              </member>
            </struct>
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
                <name>result</name>
                <value>
                  <string>OK</string>
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
   
   {"service":null,"method":"sf.message.input","id":11,"params":[{"partner":null,"message":{"text":"someone wants to talk","from":34}}]}

.. code-block:: javascript

   {"result": {"result": "OK"}, "id": 11}


.. index::
   pair: sf.message.firewall.rules.get; команда
   pair: sf.message.firewall.rules.get; firewall

Команда sf.message.firewall.rules.get
-------------------------------------

Получить текст правил :ref:`firewall <firewall>`.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, в котором находится firewall (*необязательный*)

.. describe:: firewall

   ``string`` имя свойства домена, в котором находится firewall

Результат
^^^^^^^^^

.. describe:: rules

    ``string`` текст текущих правил firewall

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
   
   {"service":null,"method":"sf.message.firewall.rules.get","id":11,"params":[{"partner":null,"firewall":"messageAnalyzer"}]}

.. code-block:: javascript

    {"result": {"rules": "do lengthCheck(minLength=1, maxLength=1000) mark invalid\nif invalid stop as INVALID\nstop as OK"}, "id": 11}


.. index::
   pair: sf.message.firewall.rules.set; команда
   pair: sf.message.firewall.rules.set; firewall

Команда sf.message.firewall.rules.set
-------------------------------------

Установить правила :ref:`firewall <firewall>`.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, в котором находится firewall (*необязательный*)

.. describe:: firewall

   ``string`` имя свойства домена, в котором находится firewall

.. describe:: rules

    ``string`` текст правил firewall

Результат
^^^^^^^^^

Нет.

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
  
   {"service":null,"method":"sf.message.firewall.rules.set","id":20,"params":[{"partner":null,"firewall":"messageAnalyzer","rules":"stop as SPAM"}]}

.. code-block:: javascript

   {"result": {}, "id": 20}

.. index::
   pair: sf.message.firewall.rules.check; команда
   pair: sf.message.firewall.rules.check; firewall

Команда sf.message.firewall.rules.check
---------------------------------------

Проверить правила :ref:`firewall <firewall>` на синтаксическую корректность.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, в котором находится firewall (*необязательный*)

.. describe:: firewall

   ``string`` имя свойства домена, в котором находится firewall

.. describe:: rules

    ``string`` текст правил firewall, которые необходимо проверить

Результат
^^^^^^^^^

Нет.

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
  
   {"service":null,"method":"sf.message.firewall.rules.check","id":24,"params":[{"partner":null,"firewall":"messageAnalyzer","rules":"stop SPAM"}]}

.. code-block:: javascript

   {"id": 24, "error": {"origin": "Fault", "message": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u0438\u043d\u0442\u0430\u043a\u0441\u0438\u0441\u0430 \u043f\u0440\u0430\u0432\u0438\u043b firewall: Expected \"as\" (at char 5), (line:1, col:6)", "code": 2008}}


.. index::
   pair: sf.message.log.fetch; команда
   pair: sf.message.log.fetch; лог сообщений

Команда sf.message.log.fetch
----------------------------

Получить из :ref:`лога сообщений <message-log>` указанный набор сообщений. При выборке
можно ограничить возвращаемые результаты по времени, а также по ID последнего полученного
сообщения (чтобы исключить получение дубликатов). 

Без указания параметров ``first``, ``last``, ``firstID`` результатом выполнения команды
будут все сообщения из указанного лога. Для повышения эффективности рекомендуется
по возможности задавать ограничения ``first`` и/или ``last``. Параметр ``firstID`` используется
для исключения возможности получения дубликатов, когда команда выполняется периодически, с целью
получить новые сообщения из лога.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, в котором находится firewall (*необязательный*)

.. describe:: log

   ``string`` имя свойства домена, в котором находится лог сообщений

.. describe:: first

    ``integer`` минимальное время получаемого сообщения, секунды, UTC (*необязательный*)

.. describe:: last

    ``integer`` максимальное время получаемого сообщения, секунды, UTC (*необязательный*)

.. describe:: firstID

    ``integer`` минимальный ID получаемого сообщения (*необязательный*)

Результат
^^^^^^^^^

.. describe:: entries

   ``Array(``:ref:`LogEntry <api-logentry>` ``)`` список записей лога сообщений

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
 
   {"service":null,"method":"sf.message.log.fetch","id":19,"params":[{"partner":null,"log":"messageLog","first":1228214550}]}

.. code-block:: javascript

   {"result": {"entries": [{"message": {"text": "Oh, darling, it's cool!", "from": 123}, "when": 1228214578, "id": 1, "tags": []}]}, "id": 19}


