/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: LogEntry.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс одно элемента лога сообщения.
 */

qx.Class.define("spamfighter.model.LogEntry", 
{
    extend: qx.core.Object,

    /**
     * Создать новую запись лога сообщений.
     *
     * @param serialized {Map} сериализованное представление записи.
     */

    construct :             function(serialized)
                            {
                                this.when = serialized['when'];
                                this.id = serialized['id'];
                                this.message = spamfighter.model.Message.unserialize(serialized['message']);
                                this.tags = serialized['tags'];
                            },

    destruct :              function()
                            {
                                this._disposeFields("id", "when");
                                this._disposeArray("tags");
                                this._disposeObjects("message");
                            },

    members : 
    {
        when : null,
        id : null,
        message : null,
        tags : null,

        /**
         * Получить время сообщения.
         *
         * @return {String} время в виде строки
         */

        getWhenAsTime : function()
        {
            var when = new Date(this.when * 1000);
            return when.toLocaleTimeString();
        }
    }
});
