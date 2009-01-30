/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: MessageWidget.js 24196 2008-12-08 09:29:22Z smir $

*/

/**
 * Элементы управления, позволяющие ввести сообщение.
 *
 * Встраиваются в какое-то окно.
 */

qx.Class.define("spamfighter.ui.MessageWidget",
{
    extend : qx.ui.groupbox.GroupBox,
    
    /**
     * Конструктор.
     *
     * @param title {String} заголовок элемента сообщения
     */
    construct :             function(title)
    {
        this.base(arguments, title);
        this.setLayout(new qx.ui.layout.Grid(4, 4).setColumnFlex(1, 2));

        this.add(new qx.ui.basic.Label("Текст:"), { row : 0, column : 0});
        this.__messageText = new qx.ui.form.TextArea("<Текст сообщения>");
        this.add(this.__messageText, { row : 0,  column : 1});

        this.add(new qx.ui.basic.Label("ID отправителя:"), { row : 1, column : 0});
        this.__messageFrom = new qx.ui.form.TextField("");
        this.add(this.__messageFrom, { row : 1,  column : 1});
    },

    destruct :              function()
                            {
                                this._disposeFields("__messageText", "__messageFrom");
                            },

    members : 
    {
        __messageText : null,
        __messageFrom : null,

        /**
         * Получить сообщение из элемента.
         *
         * @return {spamfighter.model.Message} сообщение
         */

        getMessage :        function()
                            {
                                var message = new spamfighter.model.Message();
                                message.setText(this.__messageText.getValue());
                                if (this.__messageFrom.getValue() != '')
                                    message.setFrom(parseInt(this.__messageFrom.getValue()));
                                return message;
                            }
    }
});

