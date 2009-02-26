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
   single: запуск

.. _running:

Запуск сервера
==============

Создание окружения
------------------

Перед запуском сервера необходимо создать рабочий каталог, в котором будет работать экземпляр СпамоБорца.
Выберите пользователя и группу, которые будут использоваться для данного экземпляра, создайте их в системе.
Пусть это будет пользователь и группа ``spamfighter``.

Создайте пустой каталог, владельцем которого будет пользователь ``spamfighter``. Пусть это будет каталог
``/var/lib/spamfighter``.

Запустите скрипт инициализации окружения::

  spamfighter-create --uid=spamfighter --gid=spamfighter /var/lib/spamfighter

Если Вы не собираетесь использовать OpenSSL (https), можно пропустить создание сертификата сервера::

  spamfighter-create --uid=spamfighter --gid=spamfighter --no-https /var/lib/spamfighter

Полный список параметров скрипта можно получить, запустив::

  spamfighter-create --help


По окончании работы скрипта в указанном каталоге (в нашем примере в ``/var/lib/spamfighter``) будут созданы
все необходимые файлы для работы сервера, в том числе конфигурационный файл. А также примеры скриптов
запуска и остановки: ``start.sh`` и ``stop.sh``. После запуска сервера можно обратиться из браузера
на URL: http://localhost:8000/, чтобы проверить, что всё работает правильно.

Запуск СпамоБорца осуществляется с помощью
утилиты `twistd <http://twistedmatrix.com/projects/core/documentation/man/twistd-man.html>`_, дополнительные возможности
по запуску можно прочитать в её документации. 

