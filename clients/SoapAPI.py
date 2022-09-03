import os
import json
import datetime
import textwrap
from lxml import etree
from zeep import Client
from zeep.plugins import Plugin
from zeep.wsse.username import UsernameToken
from data import SOAP_API


class SoapApiClient():
    """ 
    Клиет для отправки запросов к SOAP API 
    
    Реализованы методы:
    >>> SoapApiClient.request
    """
    @staticmethod
    def _wsse():
        try:
            client = Client(
                wsdl=SOAP_API['wsdl'],
                wsse=UsernameToken(
                    SOAP_API['wsse_login'],
                    SOAP_API['wsse_password']
                    ),
                port_name=SOAP_API['port'],
                plugins=[Soap_API_Logger()],)
            client.settings(wsse=True)
            #client.transport.session.verify = False
        except Exception as e:
            print(f"Не удалось подключиться (Причина-->> {e})")
        return client.service
    
    @staticmethod
    def request(method, **params):
        try:
            return SoapApiClient._wsse()[method](**params)
        except Exception as e:
            return f"Неверно соствлен запрос (Причина-->> {e})"

class Assertions:
    """ 
    Класс для обработки ассеротов

    Может проверить:
    >>> Assertions.assert_soap
    """
    @staticmethod
    def assert_soap(name, expected_value, error_message):
        test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        assert expected_value == name, f"Тест - {test_name} - провлен --> {error_message}:\n\tОжидаемый результат --> {expected_value}\n\t Фактический --> {name}"

class Soap_API_Logger(Plugin):
    """ 
    Класс для логирования запросов и ответов
    """
    # True or False - Для записи лога в файл

    LOG_TO_FILE = True 
    FILE_NAME = f"logs/soap_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    if LOG_TO_FILE == True:
        @classmethod
        def _write_log_to_file(cls, data):
            with open(cls.FILE_NAME, 'a', encoding='utf=8') as logger_file:
                logger_file.write(data)
    else:
        @classmethod
        def _write_log_to_file(cls, data):
            pass

    @classmethod
    def egress(cls, envelope, http_headers, binding_options, operation):
        add =  textwrap.dedent(
        '''
        Test: {test_name}
        ------------------- Request --------------------
        Operation: {operation}
        Options: {binding_options}
        Headers: {header}
        --------------------- Body ---------------------
        Body: {body}''').format(
            operation=(dict(operation)),
            binding_options = (binding_options),
            header=(json.dumps(http_headers, indent=4, ensure_ascii=True)),
            body=etree.tostring(envelope, pretty_print=True, encoding="unicode"),
            test_name = os.environ.get('PYTEST_CURRENT_TEST')
        )

        cls._write_log_to_file(add)
    
    @classmethod  
    def ingress(cls, envelope, http_headers, operation):
        add =  textwrap.dedent(
        '''
        ------------------- Response --------------------
        Headers: {header}
        --------------------- Data ----------------------
        Data: {data}
        ''').format(
            header = (json.dumps(dict(http_headers), indent=4)),
            data = etree.tostring(envelope, pretty_print=True, encoding="unicode"),
        )
        cls._write_log_to_file(add)





