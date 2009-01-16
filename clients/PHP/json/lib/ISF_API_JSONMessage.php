<?
/**
 * Интерфейс api команд работы с сообщениями
 * 
 * @version 1.0
 * @author Grishina Julia
 */

interface ISF_API_JSONMessage
{
    /**
     * Обработать сообщение и выдать результат анализа.
     * 
     * @param ISF_Message $message сообщение
     * @param string $domain поддомен, относительно которого обрабатывать сообщение
     * @return string результат анализа
     */

    public function messageInput(ISF_Message $message, $domain = null);
    
    /**
     * Получить текст правил.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param Domain $domain домен, в котором находится firewall (необязательный)
     * @return string $rules текст текущих правил firewall
     */
    
    public function messageFirewallRulesGet($firewall, $domain = null);

    /**
     * Установить правила.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param string $rules текст правил firewall
     * @param Domain $domain домен, в котором находится firewall (необязательный)
     * @return void
     */

    public function messageFirewallRulesSet($firewall, $rules, $domain = null);
    
    /**
     * Проверить правила на синтаксическую корректность.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param string $rules текст правил firewall
     * @param Domain $domain домен, в котором находится firewall
     * @return void
     */

    public function messageFirewallRulesCheck($firewall, $rules, $domain = null);
    
    /**
     * Получить из лога сообщений указанный набор сообщений. При выборке
     * можно ограничить возвращаемые результаты по времени, а также по ID последнего полученного
     * сообщения (чтобы исключить получение дубликатов).
     * Без указания параметров $first, $last, $firstID результатом выполнения команды
     * будут все сообщения из указанного лога. Для повышения эффективности рекомендуется
     * по возможности задавать ограничения $first и/или $last. Параметр $firstID используется
     * для исключения возможности получения дубликатов, когда команда выполняется периодически, с целью
     * получить новые сообщения из лога.
     *      
     * @param string $log имя свойства домена, в котором находится лог сообщений
     * @param Domain $domain домен, в котором находится firewall (необязательный)
     * @param integer $first минимальное время получаемого сообщения, секунды, UTC (необязательный)
     * @param integer $last максимальное время получаемого сообщения, секунды, UTC (необязательный)
     * @param integer $firstID минимальный ID получаемого сообщения (необязательный)
     * @return array $entries список записей лога сообщений
     */
    
    public function messageLogFetch($log, $domain = null, $first = null, $last = null, $firstID = null);
}