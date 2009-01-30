/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: MessageLog.js 24064 2008-12-01 09:16:25Z smir $

*/

/**
 * Класс доступа к серверному логу сообщений.
 */

qx.Class.define("spamfighter.model.MessageLog", 
{
    extend: qx.core.Object,

    /**
     * Создать новый лог сообщений.
     *
     * @param domain {spamfighter.model.Domain} домен, в которой находится лог
     * @param name {String} имя свойства домена, содержащего лог
     */

    construct :             function(domain, name)
                            {
                                this.__domain = domain;
                                this.__name = name;
                                this.__lastID = null;
                                this.__lastTime = null;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__name", "__lastID", "__lastTime");
                                this._disposeObjects("__domain");
                            },

    members : 
    {
        __domain : null,
        __name : null,
        __lastTime : null,
        __lastID : null,

        /**
         * Сбросить внутренние счетчики лога, начать его получение "с чистого листа".  
         */

        reset :             function()
                            {
                                this.__lastTime = this.__lastID = null;
                            },
        /**
         * Получить последние сообщения из лога.
         *
         * При первом обращении возвращаются все сообщения за последние
         * 30 секунд, при последующих - все сообщения с момента последнего 
         * обращения.
         *
         * @return {spamfighter.lib.Deferred} массив из {@link spamfighter.model.LogEntry}
         */

        fetch :             function()
                            {
                                var params = this.__domain.getDomainParams();

                                params.log = this.__name;

                                if (this.__lastTime == null)
                                {
                                    var now = new Date();
                                    params.first = Math.round(now.valueOf()/1000 - 30);
                                }
                                else
                                {
                                    params.first = this.__lastTime;
                                }

                                if (this.__lastID != null)
                                    params.firstID = this.__lastID+1;

                                var logFetched = function(result)
                                {
                                    entries = result.entries;

                                    this.__lastID = Math.max(this.__lastID == null ? 0 : this.__lastID, Math.max.apply(Math, entries.map(function(entry) { return entry['id']; })));
                                    if (this.__lastID == 0)
                                        this.__lastID = null;
                                    this.__lastTime = Math.max(this.__lastTime == null ? 0 : this.__lastTime, Math.max.apply(Math, entries.map(function(entry) { return entry['when']; })));
                                    if (this.__lastTime == 0)
                                        this.__lastTime = null;

                                    return entries.map(function (entry) { return new spamfighter.model.LogEntry(entry); });
                                };

                                return this.__domain.getServer().getAPI().call('sf.message.log.fetch', params).addCallback(qx.lang.Function.bind(logFetched, this));
                            }
    }
});

