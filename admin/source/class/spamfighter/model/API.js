/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: API.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс доступа к API сервера Спамоборца.
 */

qx.Class.define("spamfighter.model.API", 
{
    extend: qx.core.Object,

    /**
     * Создать новый экземпляр API.
     *
     * @param api_url {String} URL API сервера (JSON-RPC)
     */

    construct : function(api_url) {
            this.__api_url = api_url;
        },

    destruct : function()
        {
            this._disposeFields("__api_url");    
        },
    
    members : 
    {
        __api_url : null,

        /**
         * Вызывать метод API сервера и вернуть результат.
         *
         * @param method {String} имя метода
         * @param params {Object} хэш передаваемых параметров
         * @return {spamfighter.lib.Deferred} результат выполнения метода (хэш) или ошибка сервера 
         *      или ошибка транспорта
         */

        call :          function(method, params)
                        {
                            this.debug("API: call " + method + " with params: ");
                            this.debug(params);
                            var d = new spamfighter.lib.Deferred();

                            var rpc = new qx.io.remote.Rpc();
                            rpc.setTimeout(10000);
                            rpc.setUrl(this.__api_url);
                            rpc.callAsync(
                                function (result, ex, id)
                                {
                                    if (ex == null)
                                        d.callback(result);
                                    else
                                        d.errback(new spamfighter.model.APIError(ex.code, ex.message));
                                },
                                method, params);

                            var that = this;
                            d.addCallback(function (result) { that.debug("API: result:"); that.debug(result); return result; });
                            return d;
                        }
    }
});
