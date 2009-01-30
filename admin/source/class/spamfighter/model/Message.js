/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Message.js 24439 2008-12-13 10:05:22Z smir $

*/

/**
 * Абстракция сообщения, передаваемого или получаемого из Спамоборца.
 */


qx.Class.define("spamfighter.model.Message",
{
    extend : qx.core.Object,

    properties : 
    {
        /**
         * Текст сообщения. 
         */

        'text' : { check : 'String', nullable : true },
        
        /**
         * Идентификатор отправителя
         */

        'from' : { check : 'Integer', nullable : true }
    },
    statics :
    {
        /**
         * Десериализовать сообщение из сериализованного представления.
         *
         * @param serialized {Map} сериализованное представление
         */

        unserialize :       function(serialized)
        {
            var message = new spamfighter.model.Message();
            if ('text' in serialized)
                message.setText(serialized.text);
            if ('from' in serialized)
                message.setFrom(serialized.from);
            return message;
        }
    },
    members : 
    {
        /**
         * Сериализовать сообщение в вид, пригодный для передачи через API. 
         *
         * @return {Map} сериализованное представление
         */

        serialize :         function()
        {
            var result = {};
            if (this.getText() != null)
                result.text = this.getText();
            if (this.getFrom() != null)
                result.from = this.getFrom();

            return result;
        },

        /**
         * Проанализировать сообщение относительно домена.
         *
         * @param domain {spamfighter.model.Domain} домен
         * @param debug {Boolean ? false} включить отладочный режим?
         * @return {spamfighter.lib.Deferred} результат анализа - Map: { result: результат_анализа, log: лог_анализа (в отладочном режиме) }
         */

        analyze :           function(domain, debug)
        {
            var params = domain.getDomainParams();
            params.message = this.serialize();
            params.debug = debug ? true : false;

            return domain.getServer().getAPI().call('sf.message.input', params);
        }
    }
});

