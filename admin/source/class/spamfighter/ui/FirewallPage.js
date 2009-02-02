/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: FirewallPage.js 24439 2008-12-13 10:05:22Z smir $

*/

/**
 * Страница управления firewallом.
 */

qx.Class.define("spamfighter.ui.FirewallPage",
{
    extend : qx.ui.tabview.Page,

    construct :             function()
                            {
                                this.base(arguments, "Firewall", "spamfighter/icon/16/apps/utilities-help.png");
                                this.setLayout(new qx.ui.layout.VBox(4));

                                var firewallGroupBox = new qx.ui.groupbox.GroupBox("Firewall:");
                                firewallGroupBox.setLayout(new qx.ui.layout.HBox(4));

                                this.__firewallRulesText = new qx.ui.form.TextArea();
                                firewallGroupBox.add(this.__firewallRulesText, { flex : 1 });

                                var firewallButtonsPane = new qx.ui.container.Composite(new qx.ui.layout.VBox(4));

                                this.__firewallCheckButton = new qx.ui.form.Button("Проверить", "spamfighter/icon/22/actions/edit-undo.png");
                                firewallButtonsPane.add(this.__firewallCheckButton);

                                this.__firewallSetButton = new qx.ui.form.Button("Установить", "spamfighter/icon/22/actions/dialog-apply.png");
                                firewallButtonsPane.add(this.__firewallSetButton);

                                firewallGroupBox.add(firewallButtonsPane);

                                this.add(firewallGroupBox, { flex : 2 });

                                this.__firewallMessageWidget = new spamfighter.ui.MessageWidget("Тестовое сообщение:");
                                this.add(this.__firewallMessageWidget, { flex : 1 });

                                var firewallTestBox = new qx.ui.container.Composite(new qx.ui.layout.HBox(4));
                                var firewallTestButton = new qx.ui.form.Button("Тест", "spamfighter/icon/22/actions/media-playback-start.png");
                                this.__firewallTestResult = new qx.ui.basic.Atom("", "spamfighter/icon/16/apps/preferences-locale.png").set( { rich : true } );
                                firewallTestBox.add(firewallTestButton);
                                firewallTestBox.add(this.__firewallTestResult);

                                this.add(firewallTestBox);

                                this.__firewallCheckButton.addListener("execute", this._firewallCheck, this);
                                this.__firewallSetButton.addListener("execute", this._firewallSet, this);
                                firewallTestButton.addListener("execute", this._firewallTest, this);

                                this.__currentDomain = null;
                            },

    destruct :              function()
                            {
                                this._disposeFields("__firewallRulesText", "__firewallSetButton", "__firewallCheckButton", "__firewallMessageWidget", "__firewallTestResult", "__currentDomain");
                            },

    members :
    {
        __firewallRulesText : null,
        __firewallSetButton : null,
        __firewallCheckButton : null,
        __firewallMessageWidget : null,
        __firewallTestResult : null,
        __currentDomain : null,

        /**
         * Метод вызывается у страницы, когда изменяется текущий домен.
         *
         * @param domain {spamfighter.model.Domain} текущий домен
         */

        domainChanged :    function(domain)
                            {
                                this.__currentDomain = domain;
                                this.__firewallTestResult.setLabel('');
                                this.__currentDomain.getFirewall().addCallback(qx.lang.Function.bind(this._loadFirewallRules, this));
                            },
        /**
         * Как только свойства текущего домена загружены, загружаем правила из firewall.
         *
         * @param firewall {spamfighter.model.Firewall} firewall
         */

        _loadFirewallRules: function(firewall)
                            {
                                if (firewall == null)
                                {
                                    this.__firewallRulesText.setEnabled(false);
                                    this.__firewallCheckButton.setEnabled(false);
                                    this.__firewallSetButton.setEnabled(false);
                                    this.__firewallRulesText.setValue("<>");
                                }
                                else
                                {
                                    this.__firewallRulesText.setEnabled(true);
                                    this.__firewallCheckButton.setEnabled(true);
                                    this.__firewallSetButton.setEnabled(true);

                                    firewall.getRules().addCallback(qx.lang.Function.bind(function (rules) 
                                                {
                                                    this.__firewallRulesText.setValue(rules);
                                                }, this));
                                }
                            },

    /**
     * Реакция на кнопку "проверить правила". 
     */

    _firewallCheck :        function()
                            {
                                this.__currentDomain.getFirewall().addCallback(qx.lang.Function.bind(function (firewall)
                                            {
                                                return firewall.syntaxCheck(this.__firewallRulesText.getValue());
                                            }, this))
                                    .addCallback(function (_) { alert('OK'); })
                                    .addErrback(function (error) 
                                            { 
                                                if (error instanceof spamfighter.model.FirewallSyntaxError)
                                                {
                                                    alert(error.toString());
                                                }
                                            });
                            },

    /**
     * Реакция на кнопку "установить правила". 
     */

    _firewallSet :          function()
                            {
                                this.__currentDomain.getFirewall().addCallback(qx.lang.Function.bind(function (firewall)
                                            {
                                                return firewall.setRules(this.__firewallRulesText.getValue());
                                            }, this))
                                    .addErrback(function (error) 
                                            { 
                                                if (error instanceof spamfighter.model.FirewallSyntaxError)
                                                {
                                                    alert(error.toString());
                                                }
                                            });
                            },

    /**
     * Отправить сообщение на анализ через firewall и показать результат анализа. 
     */

    _firewallTest :         function()
                            {
                                this.__firewallTestResult.setLabel('Результат: ?');

                                this.__firewallMessageWidget.getMessage().analyze(this.__currentDomain, true)
                                    .addCallback(qx.lang.Function.bind(function(result)
                                            {
                                                this.__firewallTestResult.setLabel('Результат: <b>'+escape(result.result)+'</b>');
                                                alert(result.log);
                                            }, this))
                                    .addErrback(function(error)
                                            {
                                                alert(error.toString());
                                            });
                            }
    }
});
