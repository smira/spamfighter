/* 

 Copyright 2005 Bob Ippolito <bob@redivi.com>  
 SpamFighter, (c) 2008 NetStream LLC (http://netstream.ru/, we@netstream.ru)

 $Id: Deferred.js 24196 2008-12-08 09:29:22Z smir $

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

*/

/**
 * Реализация Deferred для qooxdoo по образу и подобию Twisted.
 *
 * Переписано под qooxdoo из MochiKit.Async (http://mochikit.com/doc/html/MochiKit/Async.html).
 *
 * Из дополнительных приятных функциональностей: если в течение 1 секунды не будет
 * обработана ошибка в Deferred (выполнение дойдет до конца цепочки callback, и останется ошибка), 
 * о ней будет сообщено на консоль, как о возможно необработанном исключении.
 */

qx.Class.define("spamfighter.lib.Deferred",
{
    extend : qx.core.Object,

    /**
     * Конструктор.
     *
     * Создает новый Deferred. Deferred еще не содержит результат и обладает
     * пустой цепочкой callbackов.
     */

    construct : function() {
            this.chain = [];
            this.fired = -1;
            this.paused = 0;
            this.results = [null, null];
            this.chained = false;
        },

    destruct :              function()
                            {
                                this._disposeArray("chain");
                                this._disposeArray("results");
                                this._disposeFields("__errorTimer");
                            },

    members : {
        chain       : null,
        fired       : null,
        paused      : null,
        results     : null,
        chained     : null,
        __errorTimer : null,

        /** 
         * В Deferred пришел результат, это может быть исключение или обычное значение.
         *
         * @param res результат Deferred
         */

        _resback: function (res) {
            this.fired = ((res instanceof Error) ? 1 : 0);
            this.results[this.fired] = res;
            this._fire();
        },

        /**
         * Проверить, не получили ли Deferred результат ранее. 
         */

        _check: function () {
            qx.core.Assert.assert(this.fired == -1, "Already fired");
        },

        /**
         * Поместить результат успешного выполнения в Deferred.
         *
         * @param res результат выполнения
         */

        callback: function (res) {
            this._check();
            qx.core.Assert.assertFalse(res instanceof spamfighter.lib.Deferred, "Deferred instances can only be chained if they are the result of a callback");
            this._resback(res);
        },
        
        /**
         * Поместить исключение (ошибку) в Deferred.
         *
         * @param res {Error} исключение
         */

        errback: function (res) {
            this._check();
            qx.core.Assert.assertFalse(res instanceof spamfighter.lib.Deferred, "Deferred instances can only be chained if they are the result of a callback");
            if (!(res instanceof Error))
                res = new Error(res);
            this._resback(res);
        },

        /**
         * Добавить функцию одновременно как callback и errback.
         *
         * @param fn {Function} функция
         * @return {Deferred} возвращает самого себя для нанизывания
         */

        addBoth: function (fn) {
            qx.core.Assert.assert(arguments.length == 1);
            return this.addCallbacks(fn, fn);
        },

        /**
         * Добавить функцию как новый callback.
         *
         * @param fn {Function} функция
         * @return {Deferred} возвращает самого себя для нанизывания
         */

        addCallback: function (fn) {
            qx.core.Assert.assert(arguments.length == 1);
            return this.addCallbacks(fn, null);
        },

        /**
         * Добавить функцию как новый errback.
         *
         * @param fn {Function} функция
         * @return {Deferred} возвращает самого себя для нанизывания
         */

        addErrback: function (fn) {
            qx.core.Assert.assert(arguments.length == 1);
            return this.addCallbacks(null, fn);
        },

        /**
         * Добавить одновременно callback и errback-функции.
         *
         * @param cb {Function} callback
         * @param eb {Function} errback
         * @return {Deferred} возвращает самого себя для нанизывания
         */

        addCallbacks: function (cb, eb) {
            if (this.chained) {
                throw new Error("Chained Deferreds can not be re-used");
            }
            this.chain.push([cb, eb]);
            if (this.fired >= 0) {
                this._fire();
            }
            return this;
        },

        /**
         * После получения результата в Deferred, бежим по последовательности callback и errback,
         * передавая результат и трансформируя его.
         */

        _fire: function () {
            var chain = this.chain;
            var fired = this.fired;
            var res = this.results[fired];
            var self = this;
            var cb = null;
            if (self.__errorTimer != null)
            {
                self.__errorTimer.stop();
                self.__errorTimer = null;
            }
            while (chain.length > 0 && this.paused === 0) {
                // Array
                var pair = chain.shift();
                var f = pair[fired];
                if (f === null) {
                    continue;
                }
                try {
                    res = f(res);
                    fired = ((res instanceof Error) ? 1 : 0);
                    if (res instanceof spamfighter.lib.Deferred) {
                        cb = function (res) {
                            self._resback(res);
                            self.paused--;
                            if ((self.paused === 0) && (self.fired >= 0)) {
                                self._fire();
                            }
                        };
                        this.paused++;
                    }
                } catch (err) {
                    fired = 1;
                    if (!(err instanceof Error)) {
                        err = new Error(err);
                    }
                    res = err;
                }
            }
            this.fired = fired;
            this.results[fired] = res;
            if (cb && this.paused) {
                // this is for "tail recursion" in case the dependent deferred
                // is already fired
                res.addBoth(cb);
                res.chained = true;
            }
            if (this.fired == 1)
            {
                self.__errorTimer = qx.event.Timer.once(this.__reportError, this, 1000);
                self.__errorTimer.start();
            }
        },

        /**
         * Сообщить о потенциально необобработанной ошибке в Deferred. 
         */

        __reportError : function()
            {
                this.warn("Unhandled error in Deferred (possibly?):");
                this.warn(this.results[this.fired]);
                self.__errorTimer = null;
            }
    },
    statics : {

        /**
         * Построить Deferred, который уже содержит результат вычисления.
         *
         * @param result результат выполнения
         * @return {Deferred}
         */

        succeed : function(result) {
            var d = new spamfighter.lib.Deferred();
            d.callback.apply(d, arguments);
            return d;
        },

        /**
         * Построить Deferred, который уже содержит ошибку (исключение).
         *
         * @param result {Error} ошибка выполнения
         * @return {Deferred}
         */

        fail : function(result) {
            var d = new spamfighter.lib.Deferred();
            d.errback.apply(d, arguments);
            return d;
        }
    }
});
