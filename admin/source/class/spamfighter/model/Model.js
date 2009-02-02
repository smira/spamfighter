/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Model.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс доступа к серверной модели анализа сообщений.
 */

qx.Class.define("spamfighter.model.Model", 
{
    extend: qx.core.Object,

    /**
     * Создать новую модель.
     *
     * @param domain {spamfighter.model.Domain} домен, в которой находится модель
     * @param name {String} имя свойства домена, содержащего модель
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
         * Обучить модель на сообщении. 
         *
         * Сообщение должно быть для модели отнесено к классу "хороших" или "плохих".
         *
         * @param message {spamfighter.model.Message} сообщение, на котором обучаем
         * @param marker {String} какое это сообщение ("good" или "bad")
         * @return {spamfighter.lib.Deferred}
         */

        train :             function(message, marker)
                            {
                                var params = this.__domain.getDomainParams();

                                params.model = this.__name;
                                params.message = message.serialize();
                                params.marker = marker;
                                return this.__domain.getServer().getAPI().call('sf.model.train', params);
                            },

        /**
         * Провести классификацию сообщения относительно модели.
         *
         * Модель возвращает класс, к которому было отнесено сообщение: класс "хороших" или "плохих".
         *
         * @param message {spamfighter.model.Message} сообщение
         * @return {spamfighter.lib.Deferred} какое это сообщение ("good" или "bad")
         */

        classify :          function(message)
                            {
                                var params = this.__domain.getDomainParams();

                                params.model = this.__name;
                                params.message = message.serialize();
                                return this.__domain.getServer().getAPI().call('sf.model.classify', params)
                                    .addCallback(function (result) { return result.marker });
                            }
    }
});

