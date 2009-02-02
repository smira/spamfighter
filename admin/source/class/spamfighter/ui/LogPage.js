/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: LogPage.js 24446 2008-12-13 10:40:25Z smir $

*/

/**
 * Страница просмотра лога сообщений.
 */

qx.Class.define("spamfighter.ui.LogPage",
{
    extend : qx.ui.tabview.Page,

    construct :             function()
                            {
                                this.base(arguments, "Лог", "spamfighter/icon/16/apps/internet-blog.png");
                                this.setLayout(new qx.ui.layout.Grid(4,4).setColumnFlex(2, 2).setRowFlex(1, 2));

                                this.add(new qx.ui.basic.Label("Лог:"), { row : 0, column : 0 });
                                this.__logSelectBox = new qx.ui.form.SelectBox();
                                this.add(this.__logSelectBox, { row : 0, column : 1});

                                this.add(new qx.ui.basic.Label("Сообщения:"), { row : 1, column : 0 });
                                this.__logModel = new qx.ui.table.model.Simple();
                                this.__logModel.setColumns(["ID", "Когда", "Текст", "Теги"]);

                                var getTableColumnModel = function(obj)
                                {
                                    return this.__tableColumnModel = new qx.ui.table.columnmodel.Resize(obj);
                                };

                                this.__logTable = new qx.ui.table.Table(this.__logModel, {
                                                    'tableColumnModel' : qx.lang.Function.bind(getTableColumnModel, this)
                                                                                         });

                                var tableResizeBehaviour = new qx.ui.table.columnmodel.resizebehavior.Default();
                            
                                this.__tableColumnModel.setBehavior(tableResizeBehaviour);

                                tableResizeBehaviour.set(0, { 'width' : 80 });
                                tableResizeBehaviour.set(1, { 'width' : 80 });
                                tableResizeBehaviour.set(2, { 'width' : '3*' });
                                tableResizeBehaviour.set(3, { 'width' : '1*' });

                                this.__logTable.getSelectionModel().setSelectionMode(qx.ui.table.selection.Model.SINGLE_INTERVAL_SELECTION);

                                this.add(this.__logTable, { row : 1, column : 1, colSpan : 2});

                                this.add(new qx.ui.basic.Label("Дообучение:"), { row : 2, column : 0 });

                                var __retrainBox = new qx.ui.container.Composite(new qx.ui.layout.HBox(4));
                                __retrainBox.add(new qx.ui.basic.Label("Обучить модель "));

                                this.__modelSelectBox = new qx.ui.form.SelectBox();
                                __retrainBox.add(this.__modelSelectBox);

                                __retrainBox.add(new qx.ui.basic.Label("как"));

                                this.__trainAsGood = new qx.ui.form.Button("хорошо", "spamfighter/icon/22/emotes/face-smile.png");
                                __retrainBox.add(this.__trainAsGood);

                               this.__trainAsBad = new qx.ui.form.Button("плохо", "spamfighter/icon/22/emotes/face-sad.png");
                                __retrainBox.add(this.__trainAsBad);

                                this.add(__retrainBox, { row : 2, column : 1, colSpan : 2});

                                this.__currentDomain = null;
                                this.__timer = null;
                                this.__log = null;

                                this.__logSelectBox.addListener("changeSelected", this._logSelectionChanged, this);
                                this.__modelSelectBox.addListener("changeSelected", this._modelSelectionChanged, this);
                                this.__logTable.getSelectionModel().addListener("changeSelection", this._modelSelectionChanged, this);
                                this.__trainAsBad.addListener("execute", qx.lang.Function.bind(this._retrainModel, this, "bad"));
                                this.__trainAsGood.addListener("execute", qx.lang.Function.bind(this._retrainModel, this, "good"));
                            },

    destruct :              function()
                            {
                                this._disposeFields("__logSelectBox", "__logModel", "__logTable", "__currentDomain", "__timer", "__log", "__tableColumnModel", 
                                            "__modelSelectBox", "__trainAsBad", "__trainAsGood");
                            },

    members :
    {
        __logSelectBox : null,
        __logModel : null,
        __logTable : null,
        __currentDomain : null,
        __timer : null,
        __log : null,
        __tableColumnModel : null,
        __modelSelectBox : null,
        __trainAsGood : null,
        __trainAsBad : null,

        /**
         * Метод вызывается у страницы, когда изменяется текущий домен.
         *
         * @param domain {spamfighter.model.Domain} текущий домен
         */

        domainChanged :    function(domain)
                            {
                                this.__currentDomain = domain;

                                this.__logSelectBox.removeAll();
                                this._logSelectionChanged();

                                this.__currentDomain.getLogs().addCallback(qx.lang.Function.bind(this._updateLogsList, this));

                                this.__modelSelectBox.removeAll();
                                this._modelSelectionChanged();

                                this.__currentDomain.getModels().addCallback(qx.lang.Function.bind(this._updateModelsList, this));
                            },
        
        /**
         * После получения списка логов сообщений текущего домена заполнить selectbox их именами. 
         *
         * @param logs {Map} хэш имен и самих логов
         */

        _updateLogsList : function(logs)
                            {
                                for (log in logs)
                                { 
                                    this.__logSelectBox.add(new qx.ui.form.ListItem(log, null, log)); 
                                }
                            },

        /**
         * Изменился выбор текущего лога в selectboxе. 
         */

        _logSelectionChanged: function()
                            {
                                if (this.__timer != null)
                                {
                                    this.__timer.stop();
                                    this.__timer = null;
                                }

                                var selectedItem = null;
                                if (this.__logSelectBox.hasChildren())
                                    selectedItem = this.__logSelectBox.getSelected();

                                this.__logModel.setData([]);
                                this.__log = null;
                                if (selectedItem != null)
                                {
                                    var log = this.__logSelectBox.getValue();
                                    this.__currentDomain.getLogs().addCallback(qx.lang.Function.bind(function(logs)
                                                {
                                                    this.__log = logs[log];
                                                    this.__log.reset();
                                                }, this)).addCallback(qx.lang.Function.bind(this._fetchEntries, this));
                                }
                            },

        /**
         * Получить новые записи из лога сообщений и отрисовать их в таблице.
         *
         * Выставляет таймер на самого себя на 3 секунды.
         */

        _fetchEntries :     function()
                            {
                                this.__timer = null;

                                this.__log.fetch()
                                    .addCallback(qx.lang.Function.bind(function(entries)
                                            {
                                                var data = entries.map(
                                                        function(item)
                                                        {
                                                            return [ item.id, item.getWhenAsTime(), item.message.getText(), item.tags.join(', ') ];
                                                        });
                                                if (this.__logModel.getRowCount() + data.length > 500)
                                                    this.__logModel.removeRows(0,  this.__logModel.getRowCount() + data.length - 500);
                                                this.__logModel.addRows(data);

                                                this.__timer = qx.event.Timer.once(this._fetchEntries, this, 3000);
                                            }, this));
                            },

        /**
         * Изменился выбор текущей модели в selectboxе. 
         */

        _modelSelectionChanged: function()
                            {

                                var selectedItem = null;
                                if (this.__modelSelectBox.hasChildren())
                                    selectedItem = this.__modelSelectBox.getSelected();
                                if (selectedItem == null || this.__logTable.getSelectionModel().isSelectionEmpty())
                                {
                                    this.__trainAsBad.setEnabled(false);
                                    this.__trainAsGood.setEnabled(false);
                                }
                                else
                                {
                                    this.__trainAsBad.setEnabled(true);
                                    this.__trainAsGood.setEnabled(true);
                                }
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
         * Реакция на кнопку "обучить модель". 
         *
         * @param marker {String} классификация для модели - "хорошее" или "плохое"
         */

        _retrainModel     : function(marker)
                            {
                                var modelName = this.__modelSelectBox.getValue();

                                var selectedTexts = [];
                                this.__logTable.getSelectionModel().iterateSelection(function(index) { selectedTexts.push(this.__logModel.getRowData(index)[2]); }, this);
                                var messages = selectedTexts.map(function(text) { var m = new spamfighter.model.Message(); m.setText(text); return m; });

                                this.__currentDomain.getModels().addCallback(function (models)
                                        {
                                            var model = models[modelName];

                                            var d = new spamfighter.lib.Deferred();
                                            messages.forEach(function (message) { d.addCallback(function(_) { model.train(message, marker); }); });

                                            d.callback(model);
                                            return d;
                                        })
                                   .addErrback(function(err)
                                           {
                                              alert("Ошибка при обучении: " + err);
                                           });
                            }

    }
});


