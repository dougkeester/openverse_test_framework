# Test steps implementation for authentication.feature
import json
import logging
import pytest
import requests

from http import HTTPStatus
from pytest_bdd import scenarios, scenario, given, when, then
# local imports
from .utils.api_info import APIInfo
from .utils.users import UserNames


LOGGER = logging.getLogger(__name__)
# The scenarios() call is necessary for Pytest to correctly execute our
# Pytest-BDD test cases.
scenarios('authentication.feature')


@scenario('authentication.feature', 'API Returns Created Response')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Name Missing')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Description Missing')
@scenario('authentication.feature',
          'API Returns Bad Request Response When Email Missing')
@scenario('authentication.feature', 'API Returns Too Many Requests')
@scenario('authentication.feature',
          'API Returns a Bearer Token To Registered User')
@scenario('authentication.feature',
          'API Returns Bad Request When Token Data Missing')
@scenario('authentication.feature',
          'API Returns Unauthorized When Token Data Incomplete')
def noop_test():
    # For now this is a NOOP. Later we may need this for specifying additional
    # logic at the start of a Scenario.
    pass


@given('I am a new API user')
def new_user(api_info):
    api_info.user_name = UserNames.generate_username()
    pass


@given('I am a registered API user')
def registered_user(api_info, import_config):
    api_info.user_name = import_config['authentication_credentials']['name']
    pass


@when('I send a correctly formatted registration request')
def correct_request(api_info, import_config, reg_request_body,
                    reg_request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    api_info.response = requests.post(api_info.url, json=reg_request_body,
                                      headers=reg_request_headers)
    # save the secret information in case we want to use it later.
    LOGGER.critical("response: " + api_info.response.text)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@when('I send a registration request with my name missing')
def no_name_request(api_info, import_config, reg_request_body,
                    reg_request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    reg_request_body['name'] = ""

    api_info.response = requests.post(api_info.url, json=reg_request_body,
                                      headers=reg_request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"name":["This field may not be blank."]}'


@when('I send a registration request with the description missing')
def no_description_request(api_info, import_config, reg_request_body,
                           reg_request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    reg_request_body['description'] = ""

    api_info.response = requests.post(api_info.url, json=reg_request_body,
                                      headers=reg_request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"description":["This field may not be blank."]}'


@when('I send a registration request with my email missing')
def no_email_request(api_info, import_config, reg_request_body,
                     reg_request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    reg_request_body['email'] = ""

    api_info.response = requests.post(api_info.url, json=reg_request_body,
                                      headers=reg_request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert api_info.response.text == \
        '{"email":["This field may not be blank."]}'


@when('I send too many registration requests in a row')
def repeated_requests_response(api_info, import_config, reg_request_body,
                               reg_request_headers):
    api_info.url = import_config['authentication_tests']['register_url']

    reg_request_body['name'] = ""

    for i in range(0, 51):
        api_info.response = requests.post(api_info.url, json=reg_request_body,
                                          headers=reg_request_headers)
        # make sure we didn't get a 500 error.
        assert api_info.response.status_code != \
            HTTPStatus.INTERNAL_SERVER_ERROR.value

        if api_info.response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
            break


@when('I request an auth token')
def send_token_request(api_info, import_config, token_request_body,
                       token_request_headers):
    api_info.url = import_config['authentication_tests']['token_url']
    api_info.response = requests.post(api_info.url, data=token_request_body,
                                      headers=token_request_headers)
    # save the secret information in case we want to use it later.
    LOGGER.critical("response: " + api_info.response.text)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@when('I request an auth token with data missing')
def send_bad_token_request(api_info, import_config, token_request_body,
                           token_request_headers):
    api_info.url = import_config['authentication_tests']['token_url']
    token_request_body['client_id'] = ""
    token_request_body['client_secret'] = ""
    token_request_body['grant_type'] = ""
    api_info.response = requests.post(api_info.url, data=token_request_body,
                                      headers=token_request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@when('I request an auth token with incomplete data')
def send_incomplete_token_request(api_info, import_config, token_request_body,
                                  token_request_headers):
    api_info.url = import_config['authentication_tests']['token_url']
    token_request_body['client_id'] = ""
    api_info.response = requests.post(api_info.url, data=token_request_body,
                                      headers=token_request_headers)
    # make sure we didn't get a 500 error.
    assert api_info.response.status_code != \
        HTTPStatus.INTERNAL_SERVER_ERROR.value


@then('I receive a 201 response')
def verify_201_response(api_info):
    assert api_info.response.status_code == HTTPStatus.CREATED.value


@then('I receive a 400 response')
def verify_400_response(api_info):
    assert api_info.response.status_code == HTTPStatus.BAD_REQUEST.value


@then('I receive a 429 response')
def verify_429_response(api_info):
    assert api_info.response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value


@then('I receive a valid auth token')
def verify_auth_token(api_info):
    assert api_info.response.status_code == HTTPStatus.OK.value
    token_data: dict = json.loads(api_info.response.text)
    assert len(token_data['access_token']) != 0
    assert token_data['expires_in'] == 43200
    assert token_data['token_type'] == 'Bearer'
    assert token_data['scope'] == 'read write'

    api_info.auth_token = token_data['access_token']


@then('I do not receive a token and get an error response')
def verify_no_token_and_error(api_info):
    assert api_info.response.status_code == HTTPStatus.BAD_REQUEST.value
    assert api_info.response.text == '{"error":"unsupported_grant_type"}'


@then('I do not receive a token and get an unauthorized response')
def verify_no_token_and_unauthorized(api_info):
    assert api_info.response.status_code == HTTPStatus.UNAUTHORIZED.value
    assert api_info.response.text == '{"error":"invalid_client"}'
