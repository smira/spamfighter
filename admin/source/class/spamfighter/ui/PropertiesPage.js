/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: PropertiesPage.js 24196 2008-12-08 09:29:22Z smir $

*/

/**
 * Страница управления свойствами домена.
 */

qx.Class.define("spamfighter.ui.PropertiesPage",
{
    extend : qx.ui.tabview.Page,

    construct :             function()
                            {
                                this.base(arguments, "Свойства", "spamfighter/icon/16/apps/utilities-archiver.png");
                                this.setLayout(new qx.ui.layout.HBox(4));

                                this.__propsList = new qx.ui.form.List();
                                this.add(this.__propsList);

                                var propsView = new qx.ui.groupbox.GroupBox("Подробности");
                                propsView.setLayout(new qx.ui.layout.Grid(4, 4).setColumnFlex(1, 2));

                                propsView.add(new qx.ui.basic.Label("Тип:"), { column : 0, row : 0});
                                this.__propClass = new qx.ui.form.TextField().set({ allowGrowY : true, readOnly : true});
                                propsView.add(this.__propClass, { column : 1, row : 0 });

                                propsView.add(new qx.ui.basic.Label("Значение:"), { column : 0, row : 1});
                                this.__propValue = new qx.ui.form.TextField().set({ allowGrowY : true, readOnly : true, width: 200});
                                propsView.add(this.__propValue, { column : 1, row : 1 });

                                propsView.add(new qx.ui.basic.Label("Интерфейсы:"), { column : 0, row : 2});
                                this.__propIfaces = new qx.ui.form.TextField().set({ allowGrowY : true, readOnly : true});
                                propsView.add(this.__propIfaces, { column : 1, row : 2 });

                                this.add(propsView, { flex : 2 });

                                this.__propsList.addListener("changeSelection", this._propListSelectionChanged, this);
                                this.__currentDomain = null;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__propsList", "__propClass", "__propValue", "__currentDomain", "__propIfaces");
                            },

    members : 
    {
        __propsList : null,
        __propClass : null,
        __propValue : null,
        __propIfaces : null,
        __currentDomain : null,

        /**
         * Метод вызывается у страницы, когда изменяется текущий домен.
         *
         * @param domain {spamfighter.model.Domain} текущий домен
         */

        domainChanged :    function(domain)
                            {
                                this.__currentDomain = domain;

                                this.__propsList.removeAll();

                                this.__currentDomain.getProperties().addCallback(qx.lang.Function.bind(this._updatePropsList, this));
                            },

        /**
         * Из домена был загружен список свойств.
         *
         * @param properties {Map} хэш имя свойства - само свойство
         */

        _updatePropsList :  function(properties)
                            {
                                for (prop in properties)
                                { 
                                    this.__propsList.add(new qx.ui.form.ListItem(prop, null, prop)); 
                                }
                            },

        /**
         * Изменился текущий элемент в списке свойств домена. 
         */

        _propListSelectionChanged : function()
                            {
                                var selectedItem = this.__propsList.getSelectedItem();
                                if (selectedItem == null)
                                {
                                    this.__propClass.setValue('');
                                    this.__propValue.setValue('');
                                    this.__propIfaces.setValue('');
                                }
                                else
                                {
                                    var self = this;

                                    this.__currentDomain.getProperties().addCallback(function (properties) 
                                            {
                                                var propInfo = properties[selectedItem.getValue()];
                                                self.__propClass.setValue(propInfo.classname);
                                                self.__propValue.setValue(propInfo.repr);
                                                self.__propIfaces.setValue(propInfo.interfaces.join(', '));
                                            });
                                }
                            }
    }
});

