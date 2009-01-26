.. SpamFighter, Copyright 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)
.. $Id$

Команды управления моделью анализа сообщений
============================================

.. index::
   pair: sf.domain.classify; команда
   pair: sf.domain.classify; модель анализа сообщений

Команда sf.model.classify
-------------------------

Классифицировать сообщение относительно :ref:`модели анализа сообщений <model>`, получить результат
классификации.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, свойства которого мы хотим получить (*необязательный*)

.. describe:: model

   ``string`` имя свойства домена, содержащего модель анализа сообщений

.. describe:: message

   :ref:`Message <api-message>` классифицируемое сообщение

.. describe:: text_attribute

   ``string`` имя атрибута сообщения, содержащего его текст (*необязательный*); 
   если параметр пропущен, его значение считается равным ``text``

Результат
^^^^^^^^^

.. describe:: marker

    ``string`` результат классификации относительно модели: ``"good"`` - "сообщение хорошее" или ``"bad"`` - сообщение "плохое"

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript

   {"service":null,"method":"sf.model.classify","id":19,"params":[{"partner":null,"domain":"comment","model":"model","message":{"text":"Let's go to Amsterdam!"}}]}

.. code-block:: javascript

   {"result": {"marker": "good"}, "id": 19}

.. index::
   pair: sf.domain.train; команда
   pair: sf.domain.train; модель анализа сообщений

Команда sf.model.train
----------------------

Обучить :ref:`модель анализа сообщений <model>` на сообщении.

Авторизация
^^^^^^^^^^^

Требуется, партнерская.

Параметры
^^^^^^^^^

.. describe:: partner

   :ref:`Partner <api-partner>` партнерская авторизация

.. describe:: domain

   :ref:`Domain <api-domain>` домен, свойства которого мы хотим получить (*необязательный*)

.. describe:: model

   ``string`` имя свойства домена, содержащего модель анализа сообщений

.. describe:: message

   :ref:`Message <api-message>` сообщение, на котором производится обучение

.. describe:: text_attribute

   ``string`` имя атрибута сообщения, содержащего его текст (*необязательный*); 
   если параметр пропущен, его значение считается равным ``text``

.. describe:: marker

    ``string`` каким является сообщение: ``"good"`` - "сообщение хорошее" или ``"bad"`` - сообщение "плохое"

Результат
^^^^^^^^^

Нет.

Пример
^^^^^^

JSON-RPC
""""""""

.. code-block:: javascript
 
   {"service":null,"method":"sf.model.train","id":18,"params":[{"partner":null,"domain":"comment","model":"model","message":{"text":"Let's go to Amsterdam!"},"marker":"good"}]}

.. code-block:: javascript

   {"result": {}, "id": 18}
