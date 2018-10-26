import os
import secrets
from typing import Generator
import pytest
from postr import config
from postr.config import update_api_key
from postr.config import git_root_dir
from postr.config import get_api_key
from postr.config import add_section
from postr.config import _current_config
from postr.config import _config_to_dict
from postr.config import pretty_print_config

TEST_CONFIG_FILE = 'postr_config_test.ini'


@pytest.yield_fixture(autouse=True)
def reset_test_config_file() -> Generator:
    config.CONFIG_FILE = TEST_CONFIG_FILE
    yield
    os.remove(os.path.join(git_root_dir(), TEST_CONFIG_FILE))


def test_get_api_key_fail() -> None:
    non_existent_key = secrets.token_hex(15)
    invalid_key = get_api_key(api='Discord', key=non_existent_key)
    assert None is invalid_key


def test_update_api_key_fail() -> None:
    old_config = _current_config()
    api, key = secrets.token_hex(15), secrets.token_hex(15)
    update_api_key(api, key, key)
    assert _config_to_dict(old_config) == _config_to_dict(_current_config())


def test_get_update_api_key() -> None:
    api, key, value = 'Discord', 'some_key', 'value'
    update_api_key(api, key, value)
    assert value == get_api_key(api, key)


def test_add_section() -> None:
    sections_count = len(_config_to_dict(_current_config()))
    add_section('a test section!')
    assert len(_config_to_dict(_current_config())) == sections_count + 1


def test_pretty_print_config() -> None:
    pretty_print_config()
