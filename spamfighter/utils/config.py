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
Питоновский враппер конфигурационных XML файлов

Превращает xml файл с конфигом в питоновскую структуру настроек


Парсинг xml
===========

    - тег со значением транслируется в строковую переменную::
        <variable>value</variable> 
        >>>variable
        "value"

    - тег c аттрибутом type по возможности будет оттранслирован в переменную данного типа::
        <variable type="int">5</variable> 
        >>>variable
        5
    - вложенные теги во вложенные объекты класса {L Cfg} где дочерние элементы представлены атрибутами::

        <parent>
            <child>value</child>
            <child2>value</child>
        </parent>
        >>>parent.child
        "value"
        >>>parent.child2
        "value"


    - Одинаковые теги с указанным id превращаются в питоновский хэш::
        <parent>
            <items id = 'first'>value1</items>
            <items id = 'second'>value2</items>
        </parent>

        >>>parent.items['first']
        "value1"


Структура xml конфига
=====================
::
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE config>
    <config>
        <global>
        <!-- основная секция. Все что находится в этой секции будет доступно как аттрибуты модуля config  -->
            <servers>
                <!-- список "боевых" серверов. -->
                <server id="1">
                    <hostname>webmorda.netstream.ru</hostname>
                </server>
            </servers>
            <some_my_params>some my value</some_my_params>
        </global>
        <local>
        </local>
        <development>
            <!-- девелоперские настройки. Эта секция будет подключена в случае если сервер на котором запущено приложение, не в списке "боевых" серверов.
            Настройки из этого раздела перезаписывают одноименные настроки из основного раздела -->
            <some_my_params>some my value</some_my_params>
        </development>
        <testing>
        <!-- тестировочный раздел. Будет подключен если приложение запущено из под trial. Настройки из этого раздела перетирают одноименные настройки
        из основного и девелоперского разделов.
            <some_my_params>some my value</some_my_params>
        </testing>
    </config>

Пример использования
====================

from spamfighter.utils import config # в случае если используется  конфигурационный файл ./config.xml - этой строки достаточно
config.load("cfg.py")
print  config.some_my_params
"""

_config = {}

from xml.dom.minidom import *
import re
import socket
import sys
import exceptions
import os

space = re.compile("\S")

def parse_file(filename):
    """
    Парсим переданный файл и возвращаем объект Cfg

    Данный метод НЕ парсит секции global, development и проч, а просто переводит xml в питоновский объект 

    Использование:
    from spamfighet.utils.config import parse_file
    cfg = parse_file('cfg.xml')
    print cfg.some_my_params

    @type filename: C{str}
    @param filename: имя файла с конфигом
    @rtype : C{Cfg}
    @return : экземпляр Cfg c настройками
    """
    try:   
        dom = parse(filename)
    except xml.parsers.expat.ExpatError:
        raise ParseException(sys.exc_info()[1], filename)
    return _parse_dom(dom)

def _parse_dom(dom):
    global space
    global _filename
    dict = Cfg()
    for elem in dom.childNodes:
        if isinstance(elem, xml.dom.minidom.Text):
            if space.match(elem.data):
                return elem.data.encode('utf8')
        elif isinstance(elem, xml.dom.minidom.Comment):
            pass
        else:
            value = _parse_dom(elem)
            if elem.hasAttribute('type'):
                value = _get_class_by_name(elem.getAttribute('type'))(value)

            if elem.tagName == 'include':
                filename = _parse_dom(elem)
                if type(filename) != type(""):
                    raise ValueError, value
                if not os.path.isabs(filename):
                    filename = os.path.normpath(os.path.join(os.path.dirname(_filename), filename))
                subconf = _load_file(filename)
                _deep_merge(dict, subconf)
            else:
                if elem.hasAttribute('id'):
                    if not dict.has_key(elem.tagName):
                        dict[elem.tagName] = Cfg()
                    dict[elem.tagName][elem.getAttribute('id')] =  value
                else:
                    dict[elem.tagName] = value
   
    if len(dom.childNodes) == 0:
        return ''
    else:
        return dict

def _get_class_by_name(name):
    if __builtins__.has_key(name):
        return __builtins__[name]
    elif globals().has_key(name):
        return globals()[name]
    else:
        raise exceptions.NameError("name %s is not defined" % name)

def _is_numeric_dict(d):
    if not isinstance(d, dict) or len(d) == 0:
        return False

    try:
        [int(val) for val in d.keys()]
    except ValueError:
        return False

    return True

def _deep_merge(old, new):
    """
    пробегаемся по всему хешу 
    """
    for key in new:
        if _is_numeric_dict(new[key]):
            old[key] = new[key]
        elif isinstance(new[key], dict) and old.has_key(key):
            old[key] = _deep_merge(old[key], new[key])
        else:
            old[key] = new[key]
        
    return old

def _get_path():
    return os.getcwd()

def load(filename = _get_path()+'/config.xml'):
    """
    Загружаем переданный файл с конфигом или конфиг по умолчанию и
    отображаем его в виде содержимого данного модуля.

    Использование:
    from spamfighther.utils import config
    config.load("cfg.xml")
    print config.some_my_param
    """

    _export_config(_load_file(filename))
    
def _load_file(filename):
    """
    Загружаем указанный файл и возвращаем его в качестве конфигурационного.
    """
    global _filename
    _filename = filename

    dom = parse(filename)

    _global = _parse_dom(dom.getElementsByTagName('global')[0])
    _config = _global

    try:
        _local  = _parse_dom(dom.getElementsByTagName('local')[0])
        _config = _deep_merge(_global, _local)
    except IndexError:
        pass
    
    _developer = os.path.exists('.svn') or os.path.exists('.git')
    # Trying to guess package root
    import inspect
    _basedir = os.path.join(os.path.dirname(inspect.getsourcefile(_load_file)), '..', '..')
    _developer = _developer or os.path.exists(os.path.join(_basedir, '.git')) or os.path.exists(os.path.join(_basedir, '.svn'))

    try:
        if _config.has_key('servers') and _config.servers.has_key('server'):
            for server in _config.servers.server.values():
                if server['hostname'] == socket.gethostname():
                    _config = _deep_merge(_config, server)
                    _developer = False
                    
            if _developer:
                _development = _parse_dom(dom.getElementsByTagName('development')[0])
                _config = _deep_merge(_config, _development)
    except IndexError:
        pass

    try:
        if sys.modules.has_key('twisted.trial.runner'):
            _testing = _parse_dom(dom.getElementsByTagName('testing')[0])
            _config = _deep_merge(_config, _testing)

            if _testing.has_key('development') and _developer:
                _config = _deep_merge(_config, _testing.development)
    except IndexError:
        pass

    return _config

def _export_config(__config):
    """
    Экспортирует указанный конфигурационный файл в качетсве атрибутов данного модуля.

    Предварительно удаляем старые отображения.
    """
    global _config

    for elem in _config:
        del sys.modules[__name__].__dict__[elem]

    _config = __config

    for elem in _config:
        sys.modules[__name__].__dict__[elem] = _config[elem]

class Cfg(dict):
    """
    Класс в который мы заворачиваем хеш. Нужен для того, чтобы нормально отображать штуки типа config.db.dsn
    """
    
    def __getattr__(self,name):
        
        if self.has_key(name):
            return self[name]
        else:
            raise AttributeError, name

    def __getitem__(self, name):
        return dict.__getitem__(self, str(name))
    
class ParseException(Exception):
    """Исключение кидаемое при попытке распарсить файл с некорректной структурой"""
    def __init__(self, message, filename):
        self.message = message
        self.filename = filename
        
    def __str__(self):
        return self.filename+": "+str(self.message)

try:
    load()
except exceptions.IOError:
    pass
