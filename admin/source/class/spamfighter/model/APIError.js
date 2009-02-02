/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: APIError.js 23907 2008-11-24 10:22:50Z smir $

*/

/**
 * Исключение при обработке запроса API
 */

qx.Class.define("spamfighter.model.APIError", 
{
    extend: Error,

    /**
     * Конструктор.
     *
     * @param code {Integer} код ошибки
     * @param message {String} текст сообщения об ошибке
     */

    construct : function(code, message)
    {
        this.code = code;
        this.message = message;
    },

    members : 
    {
        code : null,
        message : null,

        /**
         * Превратить в строчку.
         *
         * @return {String}
         */

        toString : function()
        {
            return "APIError [" + this.code + "]: " + this.message;
        }
    }

});
