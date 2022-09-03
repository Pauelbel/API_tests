import pytest
from clients.RestAPI import RestApiClient, Assertions, Validator
from tests.rest_api.schemas import USERS_LIST_RESPONSE
from data import REST_API


@pytest.mark.parametrize('url',
                         [
                            ('api/users?page=2'),
                            ('api/users?page=3'),
                            ('api/users?page=4'),

                         ])
def test_example_1(url):
    result = RestApiClient.get(f"{REST_API['url']}{url}")
    Assertions.status_code(result, 200)
    Validator.validate(result, USERS_LIST_RESPONSE)