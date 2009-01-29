<?php

/**
 * SpamFighter, Copyright 2008, 2009 NetStream LLC (http://netstream.ru/, we@netstream.ru)
 *
 * Модуль доступа к API Спамоборца с использованием Zend_XML_RPC.
 *
 * $Id$
 */

require_once('Zend/XmlRpc/Client.php');

/**
 * Интерфейс объекта сообщения, передаваемого в API Спамоборца.
 * 
 * @author Andrey Smirnov <Smirnov.Andrey@gmail.com> 
 */

interface ISF_Message
{
    /**
     * Сериализовать сообщение в представление для передачи
     * в API Спамоборца. 
     * 
     * @return array
     */

    function serialize();
}

/**
 * Класс абстракции основной единицы передачи данных - сообщения. 
 * 
 * @version 1.0
 * @author Andrey Smirnov <Smirnov.Andrey@gmail.com> 
 */

class SF_Message implements ISF_Message
{
    /**
     * Текст сообщения 
     * 
     * @var string
     * @access protected
     */

    protected $text = '';

    /**
     * ID отправителя
     *
     * @var int
     * @access protected
     */

    protected $from = null;

    /**
     * Конструктор.
     * 
     * @param string $text текст сообщения
     */

    public function __construct($text = '', $from = null)
    {
        $this->text = $text;
        $this->from = $from;
    }

    /**
     * Получить текст сообщения 
     * 
     * @return string
     */

    public function getText()
    {
        return $this->text;
    }

    /**
     * Установить текст сообщения 
     * 
     * @param string $text
     * @return SF_Message
     */

    public function setText($text)
    {
        $this->text = $text;
    }

    /**
     * Получить ID отправителя
     *
     * @return int
     */

    public function getFrom()
    {
        return $this->from;
    }

    /**
     * Установить ID отправителя
     *
     * @param int $from
     * @return SF_Message
     */

    public function setFrom($from)
    {
        $this->from = $from;

        return $this;
    }

    /**
     * Сериализовать сообщение в представление, пригодное
     * к передаче в API Спамоборца.
     * 
     * @access public
     * @return array
     */

    public function serialize()
    {
        $params = array(
            'text',
            'from',
        );

        foreach($params as $param)
            if (!is_null($this->$param))
                $ret[$param] = $this->$param;

        return $ret;
    }
}

/**
 * Ошибка API Спамоборца.
 *
 * Базовый класс, классы ошибок будут унаследованы от данного.
 * 
 * @uses Exception
 * @author Andrey Smirnov <Smirnov.Andrey@gmail.com> 
 */

class SF_API_Error extends Exception
{

}

/**
 * Класс для доступа к API Cпамоборца
 * 
 * @version 1.0
 * @author Andrey Smirnov <Smirnov.Andrey@gmail.com> 
 */

class SF_API_XMLRPC
{
    /**
     * Транспорт для доступа к API. 
     * 
     * @var Zend_XmlRpc_Client
     */

    protected $api_transport;

    /**
     * Доступ к партнерскому аккаунту Спамоборца. 
     * 
     * @var mixed
     */

    protected $partner_auth = null;

    /**
     * Конструктор.
     * 
     * @param string $api_url URL доступа к API Спамоборца 
     */

    public function __construct($api_url = "http://localhost:8000/api/xml/")
    {
        $this->api_transport = new Zend_XmlRpc_Client($api_url);
        $this->api_transport->setSkipSystemLookup(true);
    }

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
     * Получить версию сервера. 
     * 
     * @return string
     */

    public function infoVersion()
    {
        try
        {
            $result = $this->api_transport->getProxy()->sf->info->version(new Zend_XmlRpc_Value_Struct(array()));
            return $result['version'];
        }
        catch (Zend_XmlRpc_Client_FaultException $e)
        {
            throw new SF_API_Error($e->getMessage(), $e->getCode());
        }
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
        
        try
        {
            $result = $this->api_transport->getProxy()->sf->message->input($params);
            return $result['result'];
        }
        catch (Zend_XmlRpc_Client_FaultException $e)
        {
            throw new SF_API_Error($e->getMessage(), $e->getCode());
        }
    }
}
