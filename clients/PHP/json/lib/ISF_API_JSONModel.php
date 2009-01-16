<?
/**
 * Интерфейс api команд управления моделью анализа сообщений
 * 
 * @version 1.0
 * @author Grishina Julia
 */

interface ISF_API_JSONModel
{
    /**
     * Классифицировать сообщение относительно модели анализа сообщений, получить результат классификации.
     * 
     * @param ISF_Message $message классифицируемое сообщение
     * @param string  $model имя свойства домена, содержащего модель анализа сообщений
     * @param string  $text_attribute имя атрибута сообщения, содержащего его текст (необязательный); если параметр пропущен, его значение считается равным text
     * @param Domain  $domain домен, свойства которого мы хотим получить
     * @return string $marker результат классификации относительно модели: "good" - “сообщение хорошее” или "bad" - сообщение “плохое” 
     */
    
    public function modelClassify(ISF_Message $message, $model, $text_attribute = null, $domain = null);
    
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
        
    public function modelTrain(ISF_Message $message, $model, $marker, $text_attribute = null, $domain = null);
}