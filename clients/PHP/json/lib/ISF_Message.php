<?
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