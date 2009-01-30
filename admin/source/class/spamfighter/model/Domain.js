/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Domain.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Модель серверного домена.
 *
 * Домены "умеют" связываться в дерево, также в каждом
 * домене имеется некоторое количество свойств.
 */

qx.Class.define("spamfighter.model.Domain", 
{
    extend: qx.core.Object,

    /**
     * Конструктор.
     *
     * @param server {spamfighter.model.Server} сервер, в котором находится данный домен
     * @param path {String} путь к домену относительно сервера, в случае null это корневой домен
     */

    construct :             function(server, path)
                            {
                                this.__server = server;
                                this.__path = path;

                                this.__properties = null;
                                this.__subdomains =  null;
                                this.__models = null;
                                this.__firewall = null;
                                this.__logs = null;
                                
                                this.__fetchPropsD = null;
                                this.__fetchSubD = null;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__server", "__path");
                                this._disposeObjects("__fetchSubD", "__fetchPropsD", "__firewall");
                                this._disposeMap("__models");
                                this._disposeMap("__logs");
                                this._disposeMap("__properties");
                            },
    members : 
    {
        __server : null,
        __path : null,
        __properties : null,
        __subdomains : null,
        __models : null,
        __firewall : null,
        __logs : null,
        __fetchPropsD : null,
        __fetchSubD : null,

        /**
         * Получить с сервера информацию обо всех свойствах домена.
         *
         * Метод кэширует ранее собранную информацию.
         *
         * @return {spamfighter.lib.Deferred} хэш свойств домена, где ключом является имя свойства, а значением -
         *    хэш результатов команды sf.domain.get  
         */

        getProperties :     function()
                            {
                                if (this.__fetchPropsD != null)
                                {
                                    var self = this;
                                    this.__fetchPropsD.addCallback(function (_) { return self.__properties; } );
                                    return this.__fetchPropsD;
                                }

                                if (this.__properties != null)
                                    return spamfighter.lib.Deferred.succeed(this.__properties);

                                this.__properties = {};
                                this.__models = {};
                                this.__logs = {};
                                this.__firewall = null;

                                var self = this;
                                this.__fetchPropsD = this.__server.getAPI().call('sf.domain.list', self.getDomainParams())
                                            .addCallback(qx.lang.Function.bind(this.__propertiesFetched, this))
                                            .addErrback(function (res) { self.__properties = self.__models = null; self.__logs = null; return res; })
                                            .addBoth(function (res) { self.__fetchPropsD = null; return res; })
                                            .addCallback(function (_) { return self.__properties; } );

                                return this.__fetchPropsD;
                            },

        /**
         * Получен результат: список имён свойств. 
         *
         * @param result результат функции sf.domain.list
         */

        __propertiesFetched: function(result)
                            {
                                var propnames = result.properties;

                                var self = this;
                                var d = new spamfighter.lib.Deferred();
                                propnames.forEach(function (name) { d.addCallback(qx.lang.Function.bind(self.__fetchProperty, self, name)); });

                                d.callback(null);
                                return d;
                            },

        /**
         * Выборка информации о каждом свойстве. 
         *
         * @param name {String} имя свойства
         * @param _ игнорируем
         */

        __fetchProperty   : function(name, _)
                            {
                                var self = this;
                                var params = this.getDomainParams();

                                params['name'] = name;

                                return this.__server.getAPI().call('sf.domain.get', params)
                                        .addCallback(function(result) 
                                                { 
                                                    self.__properties[name] = result; 
                                                    if (result.interfaces.indexOf('IModel') != -1)
                                                        self.__models[name] = new spamfighter.model.Model(self, name);
                                                    if (result.interfaces.indexOf('IMessageFirewall') != -1)
                                                        self.__firewall = new spamfighter.model.Firewall(self, name);
                                                    if (result.interfaces.indexOf('IMessageLog') != -1)
                                                        self.__logs[name] = new spamfighter.model.MessageLog(self, name);
                                                });
                            },
        /**
         * Получить с сервера информацию обо всех поддоменах данного домена.
         *
         * Метод кэширует ранее собранную информацию.
         *
         * @return {spamfighter.lib.Deferred} хэш поддоменов, где ключом является имя домена, а значением -
         *    {@link Domain}  
         */

        getSubdomains :     function()
                            {
                                if (this.__fetchSubD != null)
                                    return this.__fetchSubD;

                                if (this.__subdomains != null)
                                    return spamfighter.lib.Deferred.succeed(this.__subdomains);

                                this.__subdomains = {};

                                var self = this;
                                var params = this.getDomainParams();

                                this.__fetchSubD = this.__server.getAPI().call('sf.domain.children', params)
                                            .addCallback(qx.lang.Function.bind(this.__subdomainsFetched, this))
                                            .addErrback(function (res) { self.__subdomains = null; return res; })
                                            .addBoth(function (res) { self.__fetchSubD = null; return res; })
                                            .addCallback(function (_) { return self.__subdomains; } );

                                return this.__fetchSubD;
                            },

        /**
         * Получен список имён поддоменов. 
         *
         * @param result результат функции sf.domain.children
         */

        __subdomainsFetched: function(result)
                            {
                                var children = result.children;

                                var self = this;
                                var d = new spamfighter.lib.Deferred();
                                children.forEach(function (name) { d.addCallback(qx.lang.Function.bind(self.__fetchSubdomain, self, name)); });

                                d.callback(null);
                                return d;
                            },

        /**
         * Построение информации о конкретном поддомене.
         *
         * @param name {String} имя поддомена
         * @param _ игнорируем
         */

        __fetchSubdomain :    function(name, _)
                            {
                                var path = this.__path;
                                
                                if (path == null)
                                    path = '';
                                else
                                    path = path + '/';

                                path = path + name;

                                this.__subdomains[name] = new spamfighter.model.Domain(this.__server, path);
                            },

        /**
         * Получить сервер, с которым связан данный домен.
         *
         * @return {spamfighter.model.Server}
         */

        getServer :         function()
                            {
                                return this.__server;
                            },

        /**
         * Получить параметры домена, которые мы можем передать в метод API сервера,
         * чтобы получить к нему доступ. Включает в себя и информацию о партнерской авторизации.
         *
         * @return {Object} хэш параметров
         */

        getDomainParams   : function()
                            {
                                var result = this.__server.getPartnerAuth();
                                if (this.__path !== null)
                                    result['domain'] = this.__path;
                                return result;
                            },

        /**
         * Получить список моделей в данном домене.
         *
         * @return {spamfighter.lib.Deferred} хэш моделей, где ключом является имя модели,
         *      а значением - {@link spamfighter.model.Model}
         */

        getModels :         function()
                            {
                                var self = this;
                                return this.getProperties().addCallback(function (_) { return self.__models; });
                            },

        /**
         * Получить список логов сообщений в данном домене.
         *
         * @return {spamfighter.lib.Deferred} хэш логов сообщений, где ключом является имя лога,
         *      а значением - {@link spamfighter.model.MessageLog}
         */

        getLogs :           function()
                            {
                                var self = this;
                                return this.getProperties().addCallback(function (_) { return self.__logs; });
                            },

        /**
         * Получить firewall в данном домене.
         *
         * @return {spamfighter.lib.Deferred} firewall ({@link spamfighter.model.Firewall})
         */

        getFirewall :       function()
                            {
                                var self = this;
                                return this.getProperties().addCallback(function (_) { return self.__firewall; });
                            }
    }
});

