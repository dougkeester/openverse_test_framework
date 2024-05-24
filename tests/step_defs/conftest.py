import json
import pytest
import requests
import yaml

# local imports
from .utils.api_info import APIInfo


# Create an instance of the APIInfo class. This should be cached through the
# entire test run.
@pytest.fixture
def api_info():
    return APIInfo("")


# This will be used to generate (and cache) an Auth Token for the API. This 
# fixture method duplicates some functionality from one of the authentication
# test cases. This is intentional so that we don't have to continually execute
# that test to get a token.
@pytest.fixture
def bearer_token(api_info, import_config, token_request_body,
                 token_request_headers):
    api_info.url = import_config['authentication_tests']['token_url']
    api_info.response = requests.post(api_info.url, data=token_request_body,
                                      headers=token_request_headers)
    token_data: dict = json.loads(api_info.response.text)

    return {'Authorization': 'Bearer ' + token_data['access_token']}


@pytest.fixture
def import_config():
    api_config = None
    with open('tests/step_defs/config.yaml', 'r') as config_yaml:
        api_config = yaml.load(config_yaml, Loader=yaml.Loader)

    return api_config


@pytest.fixture
def reg_request_body(api_info):
    # The requests library wants a JSON serializable Python object when using
    # the 'json=' parameter in a request, not an actual JSON document.
    body: dict = {}
    body['name'] = api_info.user_name
    body['description'] = "a test user for Doug's automation"
    body['email'] = "dkeester@gmail.com"

    return body


@pytest.fixture
def reg_request_headers():
    return {'Content-Type': 'application/json', 'Accept': 'application/json'}


@pytest.fixture
def token_request_body(import_config):
    body: dict = {}
    body['client_id'] = \
        import_config['authentication_credentials']['client_id']
    body['client_secret'] = \
        import_config['authentication_credentials']['client_secret']
    body['grant_type'] = \
        import_config['authentication_credentials']['grant_type']

    return body


@pytest.fixture
def token_request_headers():
    return {'Content-Type': 'application/x-www-form-urlencoded'}


# We need to define this as a way to skip tests. Pytest-BDD wants the skips
# marked in the feature file. This Python method defines the "do_not_run" tag
# and will be used to define any other custom tags for use in .feature files.
def pytest_bdd_apply_tag(tag, function):
    if tag == 'do_not_run':
        marker = pytest.mark.skip(reason="Avoid running for now.")
        marker(function)
        return True
    else:
        # Fall back to the default behavior of pytest-bdd
        return None
