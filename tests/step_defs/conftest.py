import pytest
import yaml


@pytest.fixture
def import_config():
    api_config = None
    with open('tests/step_defs/config.yaml', 'r') as config_yaml:
        api_config = yaml.load(config_yaml, Loader=yaml.Loader)

    return api_config
