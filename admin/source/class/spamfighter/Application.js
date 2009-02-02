/* 

 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Application.js 23923 2008-11-25 07:22:21Z smir $

*/

/* ************************************************************************

#asset(spamfighter/*)

************************************************************************ */

/**
 * Основной модуль приложения управления сервером СпамоБорец.
 */

qx.Class.define("spamfighter.Application",
{
  extend : qx.application.Standalone,

  members :
  {
    __desktop : null,

    /**
     * Точка входа в приложение. 
     */

    main : function()
    {
      // Call super class
      this.base(arguments);

      // Enable logging in debug variant
      if (qx.core.Variant.isSet("qx.debug", "on"))
      {
        // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Native;
        // support additional cross-browser console. Press F7 to toggle visibility
        qx.log.appender.Console;
      }

      var mainContainer = new qx.ui.container.Composite(new qx.ui.layout.VBox(5));
      this.getRoot().add(mainContainer, {edge : 0});

      var toolbar = new qx.ui.toolbar.ToolBar();
      mainContainer.add(toolbar);

      var windowManager = new qx.ui.window.Manager();
      this.__desktop = new qx.ui.window.Desktop(windowManager);
      this.__desktop.set({decorator: "main", backgroundColor: "background-pane"});
      var desktopContainer = new qx.ui.container.Composite(new qx.ui.layout.Grow());

      desktopContainer.add(this.__desktop);
      mainContainer.add(desktopContainer, { 'flex' : 1 });

      var part1 = new qx.ui.toolbar.Part();
      var newButton = new qx.ui.toolbar.Button("Новое подключение", "spamfighter/icon/22/actions/document-new.png");
      var aboutButton = new qx.ui.toolbar.Button("О программе", "spamfighter/icon/22/actions/help-faq.png");
      part1.add(newButton);
      part1.add(new qx.ui.toolbar.Separator());
      part1.add(aboutButton);
      toolbar.add(part1);

      newButton.addListener("execute", this._newConnection, this);
    },

    /**
     * Реакция на кнопку "новое подключение". 
     */

    _newConnection : function()
    {
        var win = new spamfighter.ui.NewServer(this._desktop);
        this.__desktop.add(win);
        win.addListener('createconnection', this._newServerWindow, this);
        win.open();
    },

    /**
     * Реакция на создание нового окна сервера.
     *
     * @param e {qx.event.type.Data} событие от окна подключения
     */

    _newServerWindow : function(e)
    {
        var server = e.getData();
        var serverWindow = new spamfighter.ui.ServerWindow(server);
        this.__desktop.add(serverWindow);
        serverWindow.open();
    }
  }
});
