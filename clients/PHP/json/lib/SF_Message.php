<?
require_once(SF_JSON_LIB_PATH . 'ISF_Message.php');

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