import pytest
import yaml


@pytest.fixture
def import_config():
    api_config = None
    with open('tests/step_defs/config.yaml', 'r') as config_yaml:
        api_config = yaml.load(config_yaml, Loader=yaml.Loader)

    return api_config


# We need to define this as a way to skip tests. Pytest-BDD wants the skips
# marked in the feature file.
def pytest_bdd_apply_tag(tag, function):
    if tag == 'do_not_run':
        marker = pytest.mark.skip(reason="Avoid running for now.")
        marker(function)
        return True
    else:
        # Fall back to the default behavior of pytest-bdd
        return None
