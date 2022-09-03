import requests
import datetime
import os
import json
from requests import Response



class RestApiClient():
    """ 
    Клиет для отправки запросов к REST API 
    
    Реализованы методы:
    >>> RestApiClient.get
    >>> RestApiClient.post
    """

    @staticmethod
    def get(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None ):

        return RestApiClient._send(url, data, json, headers, cookies, 'GET')

    @staticmethod
    def post(url: str, data: dict = None, json: dict = None, headers: dict = None, cookies: dict = None ):

        return RestApiClient._send(url, data, json, headers, cookies, 'POST')

    
    @staticmethod
    def _send(url: str, data: dict, json: dict, headers: dict, cookies: dict, method: str):
     
        Rest_API_Logger.add_request(url, data, json, headers, cookies, method)
        
        if headers is None:
            headers = {}
        
        if cookies is None:
            cookies = {}
        
        if data is None:
            data = {}

        if json is None:
            json = {}
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
       
        else:
            raise Exception(f'Неизестный HTTP метод  <{method}>')
        
        Rest_API_Logger.add_response(response)
        return response

class Validator:
    """ 
    Класс для проверки валидации схемы ответа
    
    Реализованы методы: 
    >>> Validator.validate(Респонс, Схема с которой надо сравнить ответ)
    """
    def validate(response, schema):
        if isinstance(response.json(), list):
            for item in response.json():
                schema.parse_obj(item)
        else:
            schema.parse_obj(response.json())
        return response

class Assertions:
    """ 
    Класс для обработки ассеротов

    Может проверить:
    >>> Assertions.status_code
    >>> Assertions.assert_json_body
    """

    def status_code(response: Response, status_code):
        """ 
        Принимает в себя
        >>> Респонс
        >>> целое чило - ожидаемый код ответа
        """
        if isinstance(response, list):
            assert response.status_code in status_code, f"Код ответа ---> {response.status_code}, ожидается ---> {status_code}"
        else:
            assert response.status_code == status_code, f"Код ответа ---> {response.status_code}, ожидается ---> {status_code}"


    def json_body(response: Response, name, expected_value, error_message):
        """ 
        Принимает в себя
        >>> Респонс
        >>> Ключ из ответа 
        >>> Ожидаемый ответ - Значение ключа
        >>> Сообщение об ошибке
        """
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Ответ не в Json формате. ответ --> {response.text}"
        
        assert response_as_dict[name] == expected_value, error_message

    def must_be_empty(response: Response, error_message):
        try:
            response_text = response.text
        except Exception as e:
            assert False, f"Ответ Не содержит текста. ответ --> {response.text}"
        assert len(response_text) == 0,  f"Ответ Должен быть пустым. ответ --> {response.text}"

class Rest_API_Logger():
    """ 
    Класс для логирования запросов и ответов
    
    """
    # True or False - Для записи лога в файл
    LOG_TO_FILE = True 

    FILE_NAME = f"logs/rest_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    if LOG_TO_FILE == True:
        @classmethod
        def _write_log_to_file(cls, data: str):
            with open(cls.FILE_NAME, 'a', encoding='utf=8') as logger_file:
                logger_file.write(data)
    else:
        @classmethod
        def _write_log_to_file(cls, data: str):
            pass

         
    @classmethod
    def add_request(cls, url: str, data: dict, json: dict, headers: dict, cookies: dict, method: str):
        test_name = os.environ.get('PYTEST_CURRENT_TEST')
        
        add = f"\n----------\n"
        add += f"Test: {test_name}\n"
        add += f"Time: {str(datetime.datetime.now())}\n"
        add += f"Request method: {method}\n"
        add += f"Request URL: {url}\n"
        add += f"Request Headers: {headers}\n"
        add += f"Request cookies: {cookies}\n"
        add += f"Request data: {data}\n"
        add += f"Request json: {json}\n"
        add += "\n"

        cls._write_log_to_file(add)

        print (add)

    @classmethod
    def add_response(cls, result: Response):
        cookies_as_dict = dict(result.cookies)
        headers_as_dict = dict(result.headers)
        result_text     = json.loads(result.text)
        
        add = f"Response code: {result.status_code}\n"
        add += f"Response headers:\n {json.dumps(headers_as_dict, indent=4, ensure_ascii=True)}\n"
        add += f"Response cookies:\n {json.dumps(cookies_as_dict, indent=4)}\n"
        add += f"Response text:\n {json.dumps(result_text, indent=4)}\n"
        add += f"\n----------\n"

        cls._write_log_to_file(add)

        print (add)
        
