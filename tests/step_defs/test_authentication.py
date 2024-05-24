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


@scenario('authentication.feature', 'API Returns Created Response')
def want_created_response(api_info):
    api_info.expected_return = HTTPStatus.CREATED
    pass


@given("I'm a new API user")
def new_user(api_info):
    api_info.user_name = UserNames.generate_username()
    pass


@when("I send a correctly formatted registration request")
def correct_request(api_info, import_config, request_body):
    api_info.url = import_config['authentication_tests']['register_url']
    headers: dict = {'Content-Type': 'application/json',
                     'Accept': 'application/json'}

    api_info.response = requests.post(api_info.url, json=request_body,
                                      headers=headers)
    # save the secret information in case we want to use it later.
    LOGGER.critical("response: " + api_info.response.text)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@then("I receive a 201 response")
def response_created(api_info):
    assert api_info.response.status_code == HTTPStatus.CREATED.value
