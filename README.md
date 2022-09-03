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
### RestAPI

Включение сбора логов в файл в ```clients/RestAPI.py``` ```class Rest_API_Logger```
Путем изменения значения переменной ```LOG_TO_FILE = True``` 
- [Пример лога](logs/log_2022-09-03_15-05-03.log)

