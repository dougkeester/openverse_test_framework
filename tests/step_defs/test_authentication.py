# Test steps implementation for authentication.feature
import logging
import pytest
import requests

from http import HTTPStatus
from pytest_bdd import scenarios, scenario, given, when, then
# local imports
from .utils.api_info import APIInfo
from .utils.users import UserNames


LOGGER = logging.getLogger(__name__)
scenarios('authentication.feature')


# Create an instance of the APIInfo class. This should be cached through the
# entire test run.
@pytest.fixture
def api_info():
    return APIInfo("")


@pytest.fixture
def request_body(api_info):
    # The requests library wants a JSON serializable Python object when using
    # the 'json=' parameter in a request, not an actual JSON document.
    body: dict = {}
    body['name'] = api_info.user_name
    body['description'] = "a test user for Doug's automation"
    body['email'] = "dkeester@gmail.com"

    return body


@pytest.fixture
def request_headers():
    return {'Content-Type': 'application/json', 'Accept': 'application/json'}



@scenario('authentication.feature', 'API Returns Created Response')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Name Missing')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Description Missing')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Email Missing')
@scenario('authentication.feature', 'API Returns Too Many Requests')
def noop_test():
    pass


@given("I'm a new API user")
def new_user(api_info):
    api_info.user_name = UserNames.generate_username()
    pass


@when("I send a correctly formatted registration request")
def correct_request(api_info, import_config, request_body, request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    api_info.response = requests.post(api_info.url, json=request_body,
                                      headers=request_headers)
    # save the secret information in case we want to use it later.
    LOGGER.critical("response: " + api_info.response.text)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@when('I send a registration request with my name missing')
def no_name_request(api_info, import_config, request_body, request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    request_body['name'] = ""

    api_info.response = requests.post(api_info.url, json=request_body,
                                      headers=request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"name":["This field may not be blank."]}'


@when('I send a registration request with the description missing')
def no_description_request(api_info, import_config, request_body,
                           request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    request_body['description'] = ""

    api_info.response = requests.post(api_info.url, json=request_body,
                                      headers=request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"description":["This field may not be blank."]}'


@when('I send a registration request with my email missing')
def no_email_request(api_info, import_config, request_body, request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    request_body['email'] = ""

    api_info.response = requests.post(api_info.url, json=request_body,
                                      headers=request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"email":["This field may not be blank."]}'


@when('I send too many registration requests in a row')
def repeated_requests_response(api_info, import_config, request_body,
                               request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    request_body['name'] = ""

    for i in range(0, 51):
        api_info.response = requests.post(api_info.url, json=request_body,
                                          headers=request_headers)
        # make sure we didn't get a 500 error.
        assert api_info.response.status_code != \
            HTTPStatus.INTERNAL_SERVER_ERROR.value

        if api_info.response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
            break


@then('I receive a 201 response')
def verify_201_response(api_info):
    assert api_info.response.status_code == HTTPStatus.CREATED.value


@then('I receive a 400 response')
def verify_400_response(api_info):
    assert api_info.response.status_code == HTTPStatus.BAD_REQUEST.value


@then('I receive a 429 response')
def verify_429_response(api_info):
    assert api_info.response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value
