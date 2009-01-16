<?
/**
 * Интерфейс api команд управления доменами
 * 
 * @version 1.0
 * @author Grishina Julia
 */

interface ISF_API_JSONDomain
{
    /**
     * Получить список свойств домена.
     * 
     * @param  Domain $domain - домен, свойства которого мы хотим получить (необязательный)
     * @return array  $result - список имен свойств домена    
     */
        
    public function domainList($domain = null);
    
    /**
     * Получить подробную информацию о свойстве домена.
     * 
     * @param  Domain $domain - домен, свойства которого мы хотим получить
     * @param  string $property_name - имя свойства домена
     * @return array  $result - string repr некоторое строковое представление свойства домена
     *                          array  interfaces список интерфейсов, которые поддерживает свойство домена
     *                          string classname класс (тип) свойства домена
     */
    
    public function domainGet($property_name, $domain = null);

    /**
     * Получить список имен поддоменов указанного домена.
     * 
     * @param  Domain $domain
     * @return array  $result
     */
    
    public function domainChildren($domain = null);
}