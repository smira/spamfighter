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

#####################################################
Документация по серверу борьбы со спамом "СпамоБорец"
#####################################################

СпамоБорец - веб-сервис, предоставляющий функции по классификации произвольных текстовых сообщений, и, 
в частности, выделения спама из общего потока сообщений.

В качестве сообщений могут рассматриваться, например, следующие виды общения, которые сегодня есть в 
социальных сетях (и веб-сайтах, имеющих элементы социальной сети):

* личные сообщения;
* чаты;
* комментарии к произвольным объектам;
* девизы, сообщения "о себе" и т.п. на страницах профиля пользователя;
* письма в службу поддержки. 

Фильтрация и классификация сообщений основывается на нескольких независимых алгоритмах; результатом классификации может являться 
классификация как самого сообщения (причём, возможно, по нескольким категориям: спам, флуд, проституция и т.п.), так и классификация 
отправителей сообщений (как авторизованных, так и неавторизованных, по тем же самым категориям: спамер, флудер и т.п.). Применение 
классификации к отправителям сообщений позволяет на раннем этапе пресекать попытки спам-рассылок и тому подобных массовых действий на сайте. 

Содержание
==========

.. toctree::
   :maxdepth: 2

   introduction
   guide/index
   api/index
   dev/index

Индексы и таблицы 
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



