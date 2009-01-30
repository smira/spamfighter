/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: FirewallSyntaxError.js 23908 2008-11-24 10:24:38Z smir $

*/

/**
 * Ошибка синтаксиса правил firewall
 */

qx.Class.define("spamfighter.model.FirewallSyntaxError", 
{
    extend: Error,

    /**
     * Конструктор.
     *
     * @param message {String} текст сообщения об ошибке
     */

    construct : function(message)
    {
        self.message = message;
    },

    members : 
    {
        /**
         * Превратить в строчку.
         *
         * @return {String}
         */

        toString : function()
        {
            return self.message;
        }
    }
});

