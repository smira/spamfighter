# -*- coding: utf-8 -*-
#
# SpamFighter, Copyright 2008, 2009 NetStream LLC (http://netstream.ru/, we@netstream.ru)
#
# This file is part of SpamFighter.
#
# SpamFighter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpamFighter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpamFighter.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Базовые интерфейсы проекта.
"""

from zope.interface import Interface, Attribute

class IDomain(Interface):
    """
    Домен - единица настроек, привязки локальных элементов 
    внутренного устройства СпамоБорца. 
    
    Все домены связаны в дерево, начинающееся главным доменом 
    (глобально известным серверу).
    
    Домен представляет из себя набор свойств и значений, при этом 
    если какое-то свойство отсутствует у данного домена, 
    он обращается за ним к домену-предку. Домен позволяет установить 
    у себя произвольные свойства, удалить (перейти на свойства главного домена).

    Доступ к доменам ограничивает партнер (L{IPartner}), который обозначает границы 
    пространства доменов, доступных данному пользователю. При каждом запросе 
    кроме указания партнера обязательно указание домена (возможно, поддомена 
    относительно главного домена партнера). 
    """
    
    def parent():
        """
        Получить предка данного домена.

        Если предка нет, будет возвращено C{None}.

        @rtype: L{IDomain}
        """

    def name():
        """
        Имя домена (относительно пути).

        Если домен корневой или не содержится в пути,
        имя может быть C{None}.

        @return: имя домена
        @rtype: C{str}
        """

    def key():
        """
        Ключ домена. Уникальное и постоянное свойство
        каждого домена.

        @return: ключ домена
        @rtype: C{str}
        """

    def children():
        """
        Получить список "дочерних" доменов.

        @return: Deferred, результат - хэш (имя домена: домен) (C{dict(}L{IDomain}C{)})
        @rtype: C{twisted.internet.defer.Deferred}
        """

    def createSubdomain(name):
        """
        Создать дочерний поддомен.

        @param name: имя поддомена
        @type name: C{str}
        @return: Deferred с созданным поддоменом, L{IDomain}
        @rtype: C{twisted.internet.defer.Deferred}
        @raise DomainDuplicateError: два поддомена с одинаковым именем не могут существовать
        """

    def walk(path):
        """
        "Пройти" по пути от текущего домена.

        @param path: путь относительно текущего домена, строка со слэшами
        @type path: C{str}
        @return: Deferred, найденный домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred}
        """

    def get(property):
        """
        Получить значение свойства домена.

        Если текущий домен не содержит информацию о данном свойстве, будет
        предпринято обращение к предку домена за данным свойством.

        @param property: имя свойства
        @type property: C{str}
        @return: значение свойства
        """

    def delete(property):
        """
        Удалить свойство из домена.

        При следующем обращении к свойству оно будет получено через предка домена,
        т.е. это эквивалентно сбросу на "значение по умолчанию".

        @param property: имя свойства
        @type property: C{str}
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """

    def set(property, value):
        """
        Установить значение свойства в домене.

        Данный метод может также создать свойство, если оно ранее не существовало 
        и переопределить свойство домена-предка.

        @param property: имя свойства
        @type property: C{str}
        @param value: значение свойства
        @return: Deferred о результате операции
        @rtype: C{twisted.internet.defer.Deferred}
        """

    def list():
        """
        Получить список имён свойств домена.

        @return: список имён свойств
        @rtype: C{list(str)}
        """

    def has(property):
        """
        Есть ли у домена указанное свойство?

        @param property: имя свойства
        @type property: C{str}
        @rtype: C{bool}
        """

class IPartnerAuthorizer(Interface):
    """
    Модуль авторизации партнеров. Способ авторизации не задается интерфейсом, но
    в результате авторизации мы должны получить партнера (L{IPartner}).
    """

    def authorize(partner_info):
        """
        Выполнить авторизацию партнера.

        @param partner_info: информация о партнере
        @return: Deferred, партнер (L{IPartner})
        @rtype: C{twisted.internet.defer.Deferred} 
        """

class IPartnerRegistrator(Interface):
    """
    Модуль регистрации партнеров с использованием логинов и паролей.
    """

    def register(login, password):
        """
        Регистрация нового партнера.

        @param login: логин партнера
        @type login: C{str}
        @param password: пароль партнера
        @type password: C{str}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.defer.Deferred}
        @raises PartnerLoginOccupiedError: такой логин уже занят (используется другим партнером)
        """

class IPartner(Interface):
    """
    Партнер - единица авторизации относительно API веб-сервиса СпамоБорца. 
    Партнер - это единица аккаунтинга запросов (кол-во запросов в сутки или 
    за другой отчетный период). 
    Партнер - это единица отслеживания любой финансовой информации.

    Партнер содержит ссылку на корневой домен партнера, ограничивая видимое 
    пространство доменов. 
    """

    def rootDomain():
        """
        Получить корневой домен партнера.

        @return: Deferred, корневой домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred} 
        """

class IAttribute(Interface):
    """
    Атрибуты характеризуют отправителя и получателя сообщений, они могут нести разную информацию.

    Атрибут является частью сообщения (L{IMessage}), тип атрибута (L{IAttributeDomain}) - его свойством.
    """

    def domain():
        """
        Получить домен атрибута.

        @return: домен атрибута
        @rtype: L{IAttributeDomain}
        """

    def value():
        """
        Получить значение атрибута.

        @return: значение атрибута
        """

    def serialize():
        """
        Получить сериализованное значение атрибута.

        @return: сериализованное значение атрибута
        """

class IAttributeDomain(Interface):
    """
    Домент (тип атрибута).
    """

    def name():
        """
        Получить имя атрибута.

        @return: имя атрибута
        @rtype: C{str}
        """

    def serialize(attribute):
        """
        Получить сериализованное значение атрибута.

        @param attribute: атрибут
        @type attribute: L{IAttribute}
        @return: сериализованное значение атрибута
        """

    def deserialize(value):
        """
        Десериализовать значение в атрибут.

        @param value: сериализованное значение
        @return: атрибут
        @rtype: L{IAttribute}
        """

class IMessageDomain(Interface):
    """
    Список доменов атрибутов, которые должны быть у сообщения.

    Такой объект хранится в домене.
    """

    def names():
        """
        Получить список имен доменов атрибутов.

        @return: список имен
        @rtype: C{list(str)}
        """

    def __getitem__(key):
        """
        Получить домен атрибута по имени.

        @param key: имя атрибута
        @type key: C{str}
        @return: атрибут домена
        @rtype: L{IAttributeDomain}
        """

class IMessage(Interface):
    """
    Сообщение - основная единица обработки для Спамоборца.

    Сообщение обладает тремя основными свойствами:
     - от кого;
     - кому;
     - текст;
     - время отправки. 

    Структурно поля "от кого" и "кому" ничем не отличаются, они описывают
    адресанта и адресата сообщения, соответственно. Поле "кому" может
    отсутствовать (например, если это сообщение - девиз пользователя на своей
    странице). Поля "от кого" и "кому" состоят из атрибутов (L{IAttribute}). 
    """

    def get(name):
        """
        Получить атрибут по имени.

        @param name: имя атрибута
        @type name: C{str}
        @return: атрибут
        @rtype: L{IAttribute}
        """

class ITaggedMessage(IMessage):
    """
    Сообщение с прицепленными к нему тэгами.
    """

    def addTag(tag):
        """
        Добавить тэг tag к сообщению.

        @param tag: тэг
        @type tag: C{str}
        """

    def getTags():
        """
        Получить все текущие тэги сообщения.

        @return: список тэгов
        @rtype: C{list(str)}
        """

    def checkHasAllTags(tags):
        """
        Проверить, содержит ли сообщение все указанные тэги.

        @param tags: список тэгов
        @type tags: C{list(str)}
        @return: содержит ли все указанные тэги?
        @rtype: C{bool}
        """

    def checkHasNoTags(tags):
        """
        Проверить, что в сообщении нет ни одного из указанных тэгов.

        @param tags: список тэгов
        @type tags: C{list(str)}
        @return: не содержит ли все указанные тэги?
        @rtype: C{bool}
        """

class IMessageAnalyzer(Interface):
    """
    Некоторый черный ящик анализа сообщений. Получает на вход
    сообщения и возвращает результат анализа.
    """
    def analyze(message, domain):
        """
        Анализировать входящие сообщение и вернуть результат анализа.

        @param message: анализируемое сообщение
        @type message: L{IMessage}
        @param domain: текущий домен
        @type domain: L{IDomain}
        @return: результат анализа
        @rtype: C{twisted.internet.defer.Deferred}
        """

class IMessageFirewall(Interface):
    """
    Маркерный интерфейс файрвола.
    """

    def getRules():
        """
        Получить текущие правила firewall'а.

        @return: текстовое представление текущих правил.
        @rtype: C{str}
        """

    def setRules(rules):
        """
        Установить новые правила анализа.

        @param rules: правила анализа
        @type rules: C{str}
        """

    def syntaxCheck(rules):
        """
        Осуществить синтаксическую проверку текста правил.

        @param rules: правила анализа
        @type rules: C{str}
        """

class IModel(Interface):
    """
    Интерфейс модели анализа сообщений.
    """

    def train(text, good):
        """
        Обучить модель на указанном тексте.

        @param text: текст, на котором обучаемся
        @type text: C{unicode}
        @param good: хороший это текст или плохой с точки зрения классификации?
        @type good: C{bool}
        @return: результат операции
        @rtype: C{Deferred}
        """

    def classify(text):
        """
        Классифицировать текст согласно модели.

        Результат классификации - текст "хороший" или "плохой" (относительно модели).

        @param text: текст, который классифируем
        @type text: C{unicode}
        @return: результат операции, C{bool}, хороший ли текст?
        @rtype: C{Deferred}
        """

class IDomainBindable(Interface):
    """
    Интерфейс объекта, который при помещении в домен должен
    узнавать о том, что он там оказался. 

    После попадания в домен у объекта будет вызван метод
    bind.
    """

    def bind(domain, name):
        """
        Извещение объекту о том, что он был помещен в домен.

        @param domain: домен
        @type domain: L{IDomain}
        @param name: имя в домене
        @type name: C{str}
        """

class IStorage(Interface):
    """
    Базовый интерфейс хранилища.
    """

class IPersistentStorage(IStorage):
    """
    Маркерный интерфейс хранилища, которое гарантирует
    сохранность данных.
    """

class IUnreliableStorage(IStorage):
    """
    Маркерный интерфейс хранилища, которое не гарантирует
    сохранность данных (в любой момент воможна потеря).
    """

class IExpirableStorage(Interface):
    """
    Ненадежное хранилище, в котором данные имеют ограниченный срок жизни. Хранилище
    хранит пары (ключ, значение).  
    """

    def get(key):
        """
        Получить значения ключа.

        Если ключ не найден (не существует, потерян, истекло время жизни), 
        возвращается исключение C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @return: Deferred значение ключа, C{str} или C{int}
        @rtype: C{twisted.internet.Deferred}
        """

    def set(key, value, expire):
        """
        Записать (перезаписать) значение ключа.

        @param key: ключ
        @type key: C{str}
        @param value: значение
        @type value: C{str} или C{int}
        @param expire: время жизни ключа в секундах, 0 - хранить "вечно"
        @type expire: C{int}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """

    def add(key, value, expire):
        """
        Добавить ключ в хранилище.

        Операция аналогична C{set}, но если ключ уже существует,
        будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: значение
        @param expire: время жизни ключа в секундах, 0 - хранить "вечно"
        @type expire: C{int}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """

    def delete(key):
        """
        Удалить ключ из хранилища. 

        Если ключ не найден, возвращается исключение C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """

    def append(key, value):
        """
        Дописать в конец значения ключа еще один элемент.
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: дописываемое значение
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.Deferred}
        """

    def incr(key, value=1):
        """
        Увеличить значение ключа на единицу (тип значения - целое число).
        Работает только над  существующими ключами, если ключ
        не существует, будет возвращена ошибка C{KeyError}.

        @param key: ключ
        @type key: C{str}
        @param value: величина инкремента
        @type value: C{int}
        @return: Deferred с новым значением ключа, C{int}
        @rtype: C{twisted.internet.Deferred}
        """

class ILogEntry(Interface):
    """
    Отдельная запись в логе сообщений.
    """

    when = Attribute("""Время и дата сообщения, UTC""")

    message = Attribute("""Сериализованное сообщение""")

    tags = Attribute("""Тэги, привязанные к сообщению""")

    id = Attribute("""ID записи""")

class IMessageLog(Interface):
    """
    Лог сообщений, проходящих через сервер.
    """

    def put(message, when=None, tags=None):
        """
        Поместить новое сообщение в лог.

        @param when: дата/время записи в логе, UTC
        @type when: C{int}
        @param message: само сообщение
        @type message: L{IMessage} или L{ITaggedMessage}
        @param tags: тэги, привзяанные к сообщению
        @type tags: C{list(str)}
        @return: Deferred о завершении операции
        @rtype: C{twisted.internet.defer.Deferred}
        """

    def fetch(first=None, last=None, firstID=None):
        """
        Произвести выборку сообщений из лога по указанным критериям выборки.

        @param first: минимальная дата возвращаемого сообщения
        @type first: C{int}
        @param last: максимальная дата возвращаемого сообщения
        @type last: C{int}
        @param firstID: минимальный ID элемента лога, который будет возвращен
        @type firstID: C{int}
        @return: Deferred с C{list(}L{ILogEntry}C{)}
        @rtype: C{twisted.internet.defer.Deferred} 
        """
