/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: NewServer.js 24196 2008-12-08 09:29:22Z smir $

*/

/**
 * Окно создания нового подключения к серверу. 
 */

qx.Class.define("spamfighter.ui.NewServer",
{
    extend: qx.ui.window.Window,

    /**
     * Конструктор. 
     */

    construct : function() 
        {
                this.base(arguments, "Новое соединение", "spamfighter/icon/22/actions/document-new.png");
                this.set({'showMaximize' : false, 'showMinimize' : false});

                var layout = new qx.ui.layout.Grid(10, 10);
                layout.setColumnAlign(0, 'right', 'top');
                layout.setColumnWidth(1, 200);
                this.setLayout(layout);

                this.add(new qx.ui.basic.Label("URL сервера:"), { row : 0, column: 0});
                this.__server_url = new qx.ui.form.TextField("http://localhost:8000/api/json/");
                this.add(this.__server_url, { row : 0, column: 1 });

                this.add(new qx.ui.basic.Label("Тип авторизации:"), { row : 1, column: 0});
                this.__authorize_kind = new qx.ui.form.SelectBox();
                this.__authorize_kind.add(new qx.ui.form.ListItem("Доверительная"));
                this.add(this.__authorize_kind, { row : 1, column: 1 });

                var paneLayout = new qx.ui.layout.HBox().set({ spacing: 4, alignX : "right" });
                var buttonPane = new qx.ui.container.Composite(paneLayout).set({paddingTop: 8});
                this.add(buttonPane, {row:2, column: 0, colSpan: 2});

                this.__okButton = new qx.ui.form.Button("OK", "spamfighter/icon/22/actions/dialog-apply.png");
                this.__okButton.addState("default");
                buttonPane.add(this.__okButton);

                var cancelButton = new qx.ui.form.Button("Отмена", "spamfighter/icon/22/actions/dialog-cancel.png");
                buttonPane.add(cancelButton);

                this.__okButton.addListener("execute", this._OkClicked, this);
                cancelButton.addListener("execute", this._CancelClicked, this);
        },

    destruct :              function()
                            {
                                this._disposeFields("__server_url", "__authorize_kind", "__okButton");
                            },
    events :
        {
            /**
             * Событие об успешном создании подключения к серверу. 
             */
            createconnection : 'qx.event.type.Data'
        },

    members : {
        __server_url : null,
        __authorize_kind : null,
        __okButton : null,

        /**
         * Реакция на нажатие кнопки "ОК".
         *
         * Пытаемся подключиться к серверу, если подключение успешно, кидаем эвент и закрываем окно.
         */

        _OkClicked : function() {
                this.__okButton.setEnabled(false);
                var server = new spamfighter.model.Server(this.__server_url.getValue());
                var that = this;
                server.getVersion()
                    .addErrback(function (err)
                        {
                            alert("Не удалось подключиться к серверу по указанному URL: " + err);
                            that.__okButton.setEnabled(true);
                            that.__server_url.focus();
                            return err;
                        })
                    .addCallback(function (_) 
                        { 
                            that.fireDataEvent('createconnection', server);
                            that.destroy();
                        });
                     },

        /**
         * Реакция на нажатие кнопки "Отмена".
         */

        _CancelClicked : function() {
                this.destroy();
                         }
    }
});
