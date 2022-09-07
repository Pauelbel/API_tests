# API_tests
Фреймворк для тестирования API

## Поддерживает 
- **RestAPI**
- **SoapAPI**
- **WebSocket**

## Установка 

```
$ git clone https://github.com/Pauelbel/API_tests.git
$ cd API_tests
$ pip install -r requirements.txt
```

## Запуск тестов 
```
python -m pytest tests/REST_API/test_example_1.py -v -s
```
## Дополнительно
### Логирование

Включение сбора логов в файл 
- ```clients/RestAPI.py``` - ```class Rest_API_Logger```
- ```clients/SoapAPI.py``` - ```class Soap_API_Logger```

Путем изменения значения переменной ```LOG_TO_FILE = True``` 
- [Пример лога для RestAPI](logs/rest_2022-09-03_16-13-31.log)
- [Пример лога для SoapAPI](logs/soap_2022-09-03_16-13-31.log)
