<?

/**
 * Ошибка транспорта API клиента.
 * 
 * @uses Exception
 * @author Grishina Julia
 */

class SF_JsonRPCTransport_Error extends Exception
{}

/**
 * Клиент для доступа к API СпамоБорца по протоколу JSON-RPC.
 *
 * @version 1.0
 * @author Grishina Julia
 */

class SF_JsonRPCTransport 
{
    /**
     * api url
     *
     * @var string
     */
    private $url;
    
    /**
     * request id
     *
     * @var integer
     */
    private $id;

    /**
     * Конструктор.
     * 
     * @param string $url api url
     * @return void
     */
    
    public function __construct($url)
    {
        $this->url = $url;
        $this->id = mktime();
    }
    
    /**
     * JsonRpc запрос и возврат результата.
     *
     * @param string $method вызываемый метод
     * @param array $params параметры
     * @return array
     */
    
    public function request($method,$params) 
    {
        if (!is_array($params))
            throw new SF_JsonRPCTransport_Error('Params are not array');
            
        $id = $this->id;
        
        $request = array(
            'method' => $method,
            'params' => array($params),
            'id' => $id
        );
        $request = json_encode($request);
        
        $context = array ('http' => array(
            'method'  => 'POST',
            'header'  => 'Content-type: application/json',
            'content' => $request
        ));
        $context  = stream_context_create($context);
        
        if ($file = file_get_contents($this->url, false, $context))
            $response = json_decode($file,true);
        else
            throw new SF_JsonRPCTransport_Error('Unable to connect to '.$this->url);

        if ($response['id'] != $id)
            throw new SF_JsonRPCTransport_Error('Incorrect response id (request id: ' . $id .', response id: '.$response['id'].')');

        if (!is_null($response['error']))
            throw new SF_JsonRPCTransport_Error($response['error']['message'], $response['error']['code']);
        
        return $response['result'];
    }
}
?>