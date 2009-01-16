<?

define(SF_JSON_LIB_PATH, dirname(__FILE__) . '/lib/');

require_once(SF_JSON_LIB_PATH . 'SF_JsonRPCTransport.php');
require_once(SF_JSON_LIB_PATH . 'SF_Message.php');
require_once(SF_JSON_LIB_PATH . 'ISF_API_JSONMessage.php');
require_once(SF_JSON_LIB_PATH . 'ISF_API_JSONInfo.php');
require_once(SF_JSON_LIB_PATH . 'ISF_API_JSONDomain.php');
require_once(SF_JSON_LIB_PATH . 'ISF_API_JSONModel.php');

/**
 * Ошибка API клиента.
 * 
 * @uses Exception
 * @author Grishina Julia
 */

class SF_API_JSON_Error extends Exception
{}

/**
 * Класс для доступа к API Cпамоборца.
 * Реализация интерфейсов api.
 * 
 * @version 1.0
 * @author Grishina Julia
 */

class SF_API_JSON implements ISF_API_JSONInfo, ISF_API_JSONDomain, ISF_API_JSONModel, ISF_API_JSONMessage
{
    /**
     * Транспорт для доступа к API. 
     * 
     * @var ApiJsonrpcClient
     */

    protected $api_transport;

    /**
     * Доступ к партнерскому аккаунту Спамоборца. 
     * 
     * @var mixed
     */

    protected $partner_auth = null;

    /**
     * Получить информацию о доступе к партнерскому аккаунту. 
     * 
     * @return mixed
     */

    public function getPartnerAuth()
    {
        return $this->partner_auth;
    }

    /**
     * Установить информацию о доступе к партнерскому аккаунту.
     * 
     * @param mixed $partner_auth 
     */

    public function setPartnerAuth($partner_auth)
    {
        $this->partner_auth = $partner_auth;

        return $this;
    }   
    
    /**
     * Транспорт.
     * 
     * @param string $command команда на выполнение
     * @param array $params массив, параметров запроса
     * @return $result
     */
    
    protected function request($command, $params)
    {
        try
        {
            $result = $this->api_transport->request($command, $params);
            return $result;
        }
        catch (SF_JsonRPCTransport_Error $e)
        {
            throw new SF_API_JSON_Error($e->getMessage(), $e->getCode());
        }      
    }

    /**
     * Конструктор.
     * 
     * @param string $api_url URL доступа к API JSON Спамоборца 
     */

    public function __construct($api_url = "http://localhost:8000/api/json/")
    {
        $this->api_transport = new SF_JsonRPCTransport($api_url);
    }
    
    /**
     * Получить версию сервера.
     * 
     * @return string версия сервера
     */
    
    public function infoVersion()
    {
        $result = $this->request('sf.info.version', array());
        return $result['version'];
    }
    
    /**
     * Получить список свойств домена.
     * 
     * @param  Domain $domain - домен, свойства которого мы хотим получить (необязательный)
     * @return array  $result - список имен свойств домена    
     */
    
    public function domainList($domain = null)
    {
        $params = array('partner' => $this->getPartnerAuth());
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $result = $this->request('sf.domain.list', $params);
        return $result['properties'];
    }
    
    /**
     * Получить подробную информацию о свойстве домена.
     * 
     * @param  Domain $domain - домен, свойства которого мы хотим получить
     * @param  string $property_name - имя свойства домена
     * @return array  $result - string repr некоторое строковое представление свойства домена
     *                          array  interfaces список интерфейсов, которые поддерживает свойство домена
     *                          string classname класс (тип) свойства домена
     */

    public function domainGet($property_name, $domain = null)
    {
        $params = array('partner' => $this->getPartnerAuth());
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;
            
        $params['name'] = (string)$property_name;

        $result = $this->request('sf.domain.get', $params);
        
        return $result;
    }
    
    /**
     * Получить список имен поддоменов указанного домена.
     * 
     * @param  Domain $domain
     * @return array  $result
     */

    public function domainChildren($domain = null)
    {
        $params = array('partner' => $this->getPartnerAuth());
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;
            
        $result = $this->request('sf.domain.children', $params);

        return $result['children'];
    }   
    
    /**
     * Классифицировать сообщение относительно модели анализа сообщений, получить результат классификации.
     * 
     * @param ISF_Message $message классифицируемое сообщение
     * @param string  $model имя свойства домена, содержащего модель анализа сообщений
     * @param string  $text_attribute имя атрибута сообщения, содержащего его текст (необязательный); если параметр пропущен, его значение считается равным text
     * @param Domain  $domain домен, свойства которого мы хотим получить
     * @return string $marker результат классификации относительно модели: "good" - “сообщение хорошее” или "bad" - сообщение “плохое” 
     */
    
    public function modelClassify(ISF_Message $message, $model, $text_attribute = null, $domain = null)
    {
        $params = array(
            'partner' => $this->getPartnerAuth(), 
            'message' => $message->serialize(), 
            'model' => (string)$model
        );
        
        if ($text_attribute !== null)
            $params['text_attribute'] = (string)$text_attribute;        

        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $result = $this->request('sf.model.classify', $params);

        return $result['marker'];
    }
    
    /**
     * Обучить модель анализа сообщений на сообщении.
     * 
     * @param ISF_Message $message классифицируемое сообщение
     * @param string  $model имя свойства домена, содержащего модель анализа сообщений
     * @param string  $marker  каким является сообщение: "good" - “сообщение хорошее” или "bad" - сообщение “плохое”
     * @param string  $text_attribute имя атрибута сообщения, содержащего его текст (необязательный); если параметр пропущен, его значение считается равным text
     * @param Domain  $domain домен, свойства которого мы хотим получить
     * @return void
     */
        
    public function modelTrain(ISF_Message $message, $model, $marker, $text_attribute = null, $domain = null)
    {
        $params = array(
            'partner' => $this->getPartnerAuth(), 
            'message' => $message->serialize(), 
            'model' => (string)$model,
            'marker' => (string)$marker,
        );

        if ($text_attribute !== null)
            $params['text_attribute'] = (string)$text_attribute;

        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $this->request('sf.model.train', $params);
    }
    
    /**
     * Обработать сообщение и выдать результат анализа.
     * 
     * @param ISF_Message $message сообщение
     * @param string $domain поддомен, относительно которого обрабатывать сообщение
     * @return string результат анализа
     */

    public function messageInput(ISF_Message $message, $domain = null)
    {
        $params = array('partner' => $this->getPartnerAuth(), 'message' => $message->serialize());
        if ($domain !== null)
            $params['domain'] = (string)$domain;
        
        $result = $this->request('sf.message.input', $params);
        
        return $result['result'];
    }
    
    /**
     * Получить текст правил.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param Domain $domain домен, в котором находится firewall
     * @return string $rules текст текущих правил firewall
     */
    
    public function messageFirewallRulesGet($firewall, $domain = null)
    {
        $params = array('partner' => $this->getPartnerAuth(), 'firewall' => (string)$firewall);
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $result = $this->request('sf.message.firewall.rules.get', $params);

        return $result['rules'];            
    }
    
    /**
     * Установить правила.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param string $rules текст правил firewall
     * @param Domain $domain домен, в котором находится firewall
     * @return void
     */
    
    public function messageFirewallRulesSet($firewall, $rules, $domain = null)
    {
        $params = array(
            'partner' => $this->getPartnerAuth(), 
            'firewall' => (string)$firewall, 
            'rules' => (string)$rules
        );
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $result = $this->request('sf.message.firewall.rules.set', $params);
    }
    
    /**
     * Проверить правила на синтаксическую корректность.
     * 
     * @param string $firewall имя свойства домена, в котором находится firewall
     * @param string $rules текст правил firewall
     * @param Domain $domain домен, в котором находится firewall
     * @return void
     */

    public function messageFirewallRulesCheck($firewall, $rules, $domain = null)
    {
        $params = array(
            'partner' => $this->getPartnerAuth(), 
            'firewall' => (string)$firewall, 
            'rules' => (string)$rules
        );
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;

        $result = $this->request('sf.message.firewall.rules.check', $params);            
    }
    
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
    
    public function messageLogFetch($log, $domain = null, $first = null, $last = null, $firstID = null)
    {
        $params = array('partner' => $this->getPartnerAuth(), 'log' => $log);
        
        if ($domain !== null)
            $params['domain'] = (string)$domain;
            
        if ($first !== null)
            $params['first'] = (int)$first;
            
        if ($last !== null)
            $params['last'] = (int)$last;
            
        if ($firstID !== null)
            $params['firstID'] = (int)$firstID;
            
        $result = $this->request('sf.message.log.fetch', $params);

        return $result['entries'];
    }
}

?>