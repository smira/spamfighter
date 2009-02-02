/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: ModelPage.js 24196 2008-12-08 09:29:22Z smir $

*/

/**
 * Страница управления моделью анализа сообщений.
 */

qx.Class.define("spamfighter.ui.ModelPage",
{
    extend : qx.ui.tabview.Page,

    construct :             function()
                            {
                                this.base(arguments, "Модели", "spamfighter/icon/16/apps/utilities-dictionary.png");
                                this.setLayout(new qx.ui.layout.Grid(4,4).setColumnFlex(2, 2).setRowFlex(5, 2));

                                this.add(new qx.ui.basic.Label("Модель:"), { row : 0, column : 0 });
                                this.__modelSelectBox = new qx.ui.form.SelectBox();
                                this.add(this.__modelSelectBox, { row : 0, column : 1});

                                this.__modelMessageWidget = new spamfighter.ui.MessageWidget("Сообщение:")
                                this.add(this.__modelMessageWidget, { row : 1, column : 0, colSpan : 3});

                                this.__modelTrainButton = new qx.ui.form.Button("Обучить как", "spamfighter/icon/22/actions/list-add.png");
                                this.add(this.__modelTrainButton, { row : 2, column : 0});

                                this.__modelTrainKind = new qx.ui.form.SelectBox();
                                this.__modelTrainKind.add(new qx.ui.form.ListItem("Хорошо", null, "good"));
                                this.__modelTrainKind.add(new qx.ui.form.ListItem("Плохо", null, "bad"));
                                this.add(this.__modelTrainKind, { row : 2, column : 1});
                                
                                this.__modelClassifyButton = new qx.ui.form.Button("Классифицировать", "spamfighter/icon/22/actions/system-run.png");
                                this.add(this.__modelClassifyButton, { row : 3, column : 0});

                                this.add(new qx.ui.basic.Label("Лог действий:"), { row : 4, column : 0 });
                                this.__modelLog = new qx.ui.form.TextArea();
                                this.__modelLog.setReadOnly(true);
                                this.add(this.__modelLog, { row : 5, column : 0, colSpan : 3});

                                this.__currentDomain = null;

                                this.__modelTrainButton.addListener("execute", this._trainModel, this);
                                this.__modelClassifyButton.addListener("execute", this._classifyModel, this);
                                this.__modelSelectBox.addListener("changeSelected", this._modelSelectionChanged, this);
                            },

    destruct :              function()
                            {
                                this._disposeFields("__modelSelectBox", "__modelMessageWidget", "__modelTrainKind", "__currentDomain", "__modelLog", "__modelTrainButton", "__modelClassifyButton");
                            },

    members :
    {
        __modelSelectBox : null,
        __modelMessageWidget : null,
        __modelTrainKind : null,
        __modelLog : null,
        __modelTrainButton : null,
        __modelClassifyButton : null,
        __currentDomain : null,

        /**
         * Метод вызывается у страницы, когда изменяется текущий домен.
         *
         * @param domain {spamfighter.model.Domain} текущий домен
         */

        domainChanged :    function(domain)
                            {
                                this.__currentDomain = domain;

                                this.__modelSelectBox.removeAll();
                                this._modelSelectionChanged();

                                this.__currentDomain.getModels().addCallback(qx.lang.Function.bind(this._updateModelsList, this));
                            },
        
        /**
         * После получения списка моделей текущего домена заполнить selectbox их именами. 
         *
         * @param models {Map} хэш имен и самих моделей
         */

        _updateModelsList : function(models)
                            {
                                for (model in models)
                                { 
                                    this.__modelSelectBox.add(new qx.ui.form.ListItem(model, null, model)); 
                                }
                            },

        /**
         * Изменился выбор текущей модели в selectboxе. 
         */

        _modelSelectionChanged: function()
                            {

                                var selectedItem = null;
                                if (this.__modelSelectBox.hasChildren())
                                    selectedItem = this.__modelSelectBox.getSelected();
                                if (selectedItem == null)
                                {
                                    this.__modelTrainButton.setEnabled(false);
                                    this.__modelClassifyButton.setEnabled(false);
                                    this.__modelTrainKind.setEnabled(false);
                                }
                                else
                                {
                                    this.__modelTrainButton.setEnabled(true);
                                    this.__modelClassifyButton.setEnabled(true);
                                    this.__modelTrainKind.setEnabled(true);
                                }
                            },

        /**
         * Реакция на кнопку "обучить модель". 
         */

        _trainModel :       function()
                            {
                                var self = this;
                                var marker = this.__modelTrainKind.getValue();
                                var model = self.__modelSelectBox.getValue();
                                var message = self.__modelMessageWidget.getMessage();

                                this.__currentDomain.getModels().addCallback(function (models)
                                        {
                                            return models[model].train(message, marker);
                                        })
                                    .addCallback(function (_) 
                                        {
                                            self.__modelLog.setValue(self.__modelLog.getValue() + "Модель " + model + 
                                                " успешно обучена на сообщении \"" + message.getText() + "\" [\"" + marker + "\"].\n");
                                        })
                                    .addErrback(function (err)
                                        {
                                            self.__modelLog.setValue(self.__modelLog.getValue() + "Ошибка при обучении\n");
                                            return err;
                                        });
                            },
 
        /**
         * Реакция на кнопку "классифицировать по модели". 
         */

        _classifyModel :    function()
                            {
                                var self = this;
                                var model = self.__modelSelectBox.getValue();
                                var message = self.__modelMessageWidget.getMessage();

                                this.__currentDomain.getModels().addCallback(function (models)
                                        {
                                            return models[model].classify(message);
                                        })
                                    .addCallback(function (marker) 
                                        {
                                            self.__modelLog.setValue(self.__modelLog.getValue() + "Модель " + model + " классифицировала сообщение \"" + message.getText() + "\" как \"" + marker + "\".\n");
                                        })
                                    .addErrback(function (err)
                                        {
                                            self.__modelLog.setValue(self.__modelLog.getValue() + "Ошибка при классификации\n");
                                            return err;
                                        });

                            }
    }
});


