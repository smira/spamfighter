/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Firewall.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс доступа к серверному firewall, который осуществляет анализ сообщений.
 */

qx.Class.define("spamfighter.model.Firewall", 
{
    extend: qx.core.Object,

    /**
     * Создать новый firewall.
     *
     * @param domain {spamfighter.model.Domain} домен, в которой находится firewall
     * @param name {String} имя свойства домена, содержащего firewall
     */

    construct :             function(domain, name)
                            {
                                this.__domain = domain;
                                this.__name = name;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__name");
                                this._disposeObjects("__domain");
                            },

    members : 
    {
        __domain : null,
        __name : null,

        /**
         * Получить текущие правила firewall.
         *
         * @return {spamfighter.lib.Deferred} текст правил (строка)
         */

        getRules :          function()
                            {
                                var params = this.__domain.getDomainParams();

                                params.firewall = this.__name;
                                return this.__domain.getServer().getAPI().call('sf.message.firewall.rules.get', params).
                                    addCallback(function (result)
                                            {
                                                return result.rules;
                                            });
                            },

        /**
         * Установить правила firewall.
         *
         * @param rules {String} новые правила
         * @return {spamfighter.lib.Deferred} результат операции
         */

        setRules :          function(rules)
                            {
                                var params = this.__domain.getDomainParams();

                                params.firewall = this.__name;
                                params.rules = rules;
                                return this.__domain.getServer().getAPI().call('sf.message.firewall.rules.set', params)
                                    .addErrback(function (error) { 
                                            if (error instanceof spamfighter.model.APIError && error.code == 2008) 
                                                return new spamfighter.model.FirewallSyntaxError(error.message); 
                                            return error;
                                        });
                            },

        /**
         * Проверить синтаксис правил firewall.
         *
         * @param rules {String} новые правила
         * @return {spamfighter.lib.Deferred} результат операции
         */

        syntaxCheck :       function(rules)
                            {
                                var params = this.__domain.getDomainParams();

                                params.firewall = this.__name;
                                params.rules = rules;
                                return this.__domain.getServer().getAPI().call('sf.message.firewall.rules.check', params)
                                    .addErrback(function (error) { 
                                            if (error instanceof spamfighter.model.APIError && error.code == 2008) 
                                                return new spamfighter.model.FirewallSyntaxError(error.message); 
                                            return error;
                                        });
                            }
    }
});

