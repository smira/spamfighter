/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Server.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс, представляющий собой сервер Спамоборца.
 */

qx.Class.define("spamfighter.model.Server", 
{
    extend: qx.core.Object,

    /**
     * Конструктор.
     *
     * @param url {String}: URL API сервера (JSON-RPC)
     */

    construct :             function(url)
                            {
                                this.__url = url;
                                this.__api = new spamfighter.model.API(this.__url);
                                this.__version = null;
                                this.__versionDeferred = null;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__url", "__version");
                                this._disposeObjects("__api", "__versionDeferred");
                            },

    members : 
    {
        __url : null,
        __api : null,
        __version : null,
        __versionDeferred : null,

        /**
         * Получить URL сервера.
         *
         * @return {String}
         */

        getUrl :            function()
                            {
                                return this.__url;
                            },

        /**
         * Получить версию сервера.
         *
         * Метод кэширует версию сервера, если она была запрошена ранее.
         *
         * @return {spamfighter.lib.Deferred} версия сервера (строка)
         */

        getVersion :        function()
                            {
                                if (this.__version != null)
                                    return spamfighter.lib.Deferred.succeed(this.__version);
                                
                                if (this.__versionDeferred != null)
                                    return this.__versionDeferred;

                                var that = this;
                                return this.__versionDeferred = this.__api.call('sf.info.version', {}).addCallback(function (result) { that.__version = result.version; that.__versionDeferred = null; return that.__version; } );
                            },

        /**
         * Получить API для доступа к серверу.
         *
         * @return {spamfighter.model.API}
         */

        getAPI :            function()
                            {
                                return this.__api;
                            },

        /**
         * Получить корневой домен сервера (относительно текущей авторизации).
         *
         * @return {spamfighter.model.Domain}
         */

        getRootDomain :     function()
                            {
                                return new spamfighter.model.Domain(this, null);
                            },

        /**
         * Получить часть параметром вызова команды, обеспечивающую авторизацию
         * относительно текущего партнера.
         *
         * @return {Object} хэш параметров
         */

        getPartnerAuth :    function()
                            {
                                return { partner : null };
                            }
    }
});

