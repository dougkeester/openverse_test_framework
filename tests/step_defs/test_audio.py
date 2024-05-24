# Test steps implementation for audio.feature
import json
import logging
import requests

from http import HTTPStatus
from pytest_bdd import scenarios, scenario, given, when, then
from uuid import UUID


LOGGER = logging.getLogger(__name__)
# The scenarios() call is necessary for Pytest to correctly execute our
# Pytest-BDD test cases.
scenarios('audio.feature')


@scenario('audio.feature', 'Use the API to search for audio files')
@scenario('audio.feature',
          'Use the API to retrieve stats about content providers')
def noop_test():
    # For now this is a NOOP. Later we may need this for specifying additional
    # logic at the start of a Scenario.
    pass

@given('I am a registered API user')
def registered_user(api_info, import_config):
    api_info.user_name = import_config['authentication_credentials']['name']
    pass


@when('I search using the audio API correctly')
def successful_search(api_info, bearer_token, import_config):
    payload: dict = {'page': 1, 'page_size': 10, 'q': "piano solo"}
    api_info.url = import_config['audio_tests']['search_url']

    api_info.response = requests.get(api_info.url, params=payload,
                                     headers=bearer_token)

    # make sure we got a good response.
    assert api_info.response.status_code == HTTPStatus.OK.value


@when('I call the stats endpoint correctly')
def successful_stats_call(api_info, bearer_token, import_config):
    api_info.url = import_config['audio_tests']['stats_url']

    api_info.response = requests.get(api_info.url, headers=bearer_token)

    # make sure we got a good response.
    assert api_info.response.status_code == HTTPStatus.OK.value


@then('I receive good search results data')
def verify_search_results(api_info):
    response_body: dict = json.loads(api_info.response.text)
    assert response_body['result_count'] >= 200
    assert response_body['page_size'] == 10
    assert response_body['page'] == 1
    # bonus test
    assert UUID(response_body['results'][0]['id'], version=4).hex == \
        response_body['results'][0]['id'].replace('-', '')


@then('I receive good stats results data')
def verify_stats_results(api_info):
    response_body: list = json.loads(api_info.response.text)
    assert response_body[0]['media_count'] > 0
    assert response_body[1]['media_count'] > 0
    assert response_body[2]['media_count'] > 0
