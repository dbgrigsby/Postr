from postr.config import update_api_key
from postr.config import get_api_key


def test_config_parser() -> None:
    api, key, value = 'Discord', 'some_key', 'value'
    update_api_key(api, key, value)
    assert value == get_api_key(api, key)
