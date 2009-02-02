/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: ServerWindow.js 24196 2008-12-08 09:29:22Z smir $

*/

/**
 * Основное окно работы с сервером.
 */

qx.Class.define("spamfighter.ui.ServerWindow",
{
    extend : qx.ui.window.Window,

    /**
     * Конструктор.
     *
     * @param server {spamfighter.model.Server} сервер, которым мы будем управлять
     */

    construct :             function(server)
                            {
                                this.__server = server;
                                this.__rootDomain = this.__server.getRootDomain();
                                this.__currentDomain = this.__rootDomain;

                                this.base(arguments, "Сервер: " + this.__server.getUrl(), "spamfighter/icon/22/apps/utilities-terminal.png");
                                this.set({'showMinimize' : false, 'padding' : 4});
                                this.setLayout(new qx.ui.layout.VBox(4));

                                var label = new qx.ui.basic.Atom("Сервер: " + this.__server.getUrl() + ", авторизация: доверительная, версия: ", "icon/22/devices/computer.png");
                                this.add(label);

                                this.__server.getVersion().addCallback(function (version) { label.setLabel(label.getLabel() + version);});

                                var pane = new qx.ui.splitpane.Pane('horizontal');
                                var leftBox = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));
                                var rightTab = new qx.ui.tabview.TabView();

                                leftBox.add(new qx.ui.basic.Label("Домены:"));
                                this.__domainTree = new qx.ui.tree.Tree();
                                leftBox.add(this.__domainTree, { flex : 1 });

                                var refreshButton = new qx.ui.form.Button("Обновить", "spamfighter/icon/22/actions/view-refresh.png");
                                leftBox.add(refreshButton);
                                   
                                this.__propertiesPage = new spamfighter.ui.PropertiesPage();
                                rightTab.add(this.__propertiesPage);

                                this.__firewallPage = new spamfighter.ui.FirewallPage();
                                rightTab.add(this.__firewallPage);

                                this.__modelPage = new spamfighter.ui.ModelPage();
                                rightTab.add(this.__modelPage);

                                this.__logPage = new spamfighter.ui.LogPage();
                                rightTab.add(this.__logPage);

                                pane.add(leftBox, 0);
                                pane.add(rightTab, 1);
                                this.add(pane, { flex : 1});

                                this.__domainTree.addListener("changeSelection", this._domainChanged, this);
                                refreshButton.addListener("execute", this._refreshAll, this);

                                this._buildDomainTree();
                                
                            },

    destruct :              function()
                            {
                                this._disposeFields("__server", "__currentDomain", "__domainTree", "__propertiesPage", "__modelPage", "__firewallPage", "__logPage");
                            },

    members : 
    {
        __server : null,
        __currentDomain : null,
        __domainTree : null,
        __propertiesPage : null,
        __modelPage : null,
        __firewallPage : null,
        __logPage : null,

        /**
         * По корневому домену сервера построим дерево поддоменов. 
         */

        _buildDomainTree :  function()
                            {
                                this.__domainTree.setRoot(null);

                                var root = new qx.ui.tree.TreeFolder("Корень");
                                root.setOpen(true);
                                root.__domain = this.__rootDomain;
                                this.__domainTree.setRoot(root);

                                this._syncDomainTree(root, this.__rootDomain);

                                this.__domainTree.select(root);

                            },

        /**
         * Скопировать дерево доменов сервера на дерево в элементе управления.
         *
         * @param tree {qx.ui.tree.AbstractTreeItem} элемент дерева
         * @param domain {spamfighter.model.Domain} соответствующий ему поддомен
         */

        _syncDomainTree :   function(tree, domain)
                            {
                                var _copyDomainTree = function(tree, subdomains)
                                    {
                                        for (name in subdomains)
                                        {
                                            var subdomain = subdomains[name];
                                            var elem = null;
                                            elem = new qx.ui.tree.TreeFolder(name);
                                            elem.__domain = subdomain;
                                            this._syncDomainTree(elem, subdomain);
                                            tree.add(elem);
                                        }
                                    };

                                domain.getSubdomains().addCallback(qx.lang.Function.bind(_copyDomainTree, this, tree));  
                            },

        /**
         * Изменился текущий выбранный домен в списке доменов. 
         */

        _domainChanged  :   function()
                            {
                                this.__currentDomain = this.__domainTree.getSelectedItem().__domain;

                                this.__propertiesPage.domainChanged(this.__currentDomain);
                                this.__modelPage.domainChanged(this.__currentDomain);
                                this.__firewallPage.domainChanged(this.__currentDomain);
                                this.__logPage.domainChanged(this.__currentDomain);
                            },

        /**
         * Реакция на кнопку "обновить". 
         */

        _refreshAll :       function()
                            {
                                this.__rootDomain = this.__currentDomain = this.__server.getRootDomain();
                                this._buildDomainTree();
                            }
    }
});
