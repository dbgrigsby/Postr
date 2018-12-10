import os.path
import pprint
from configparser import ConfigParser
from typing import Any
from typing import Mapping
from typing import Optional
from typing import List
from typing import Dict
from postr import postr_logger
from postr.git_tools import git_root_dir

# Creates or reads the authentication config file
CONFIG_FILE = 'postr_config.ini'
DEFAULT_CONFIG: Mapping[str, Mapping[str, Any]] = {
    'Discord': {
        'client_secret': '',
        'bot_token': '',
        'default_channel': '',
    },
    'Facebook': {
        'has_token': 'false',
        'app_id': '',
        'app_secret': '',
        'app_token': '',
        'access_token': '',
        'client_token': '',
        'password': '',
        'email': '',
    },
    'Twitter': {
        'ACCESS_TOKEN': '',
        'ACCESS_TOKEN_SECRET': '',
        'CONSUMER_KEY': '',
        'CONSUMER_SECRET': '',
    },
    'Reddit': {
        'subreddit': '',
        'client_id': '',
        'refresh_token': '',
    },
    'Slack': {
        'default_channel': '',
        'API_TOKEN': '',
    },
    'Instagram': {
        'USERNAME': '',
        'PASSWORD': '',
    },
    'Tumblr': {
        'consumer_key': '',
        'consumer_secret': '',
        'auth_token': '',
        'auth_token_secret': '',
    },
    'YouTube': {
        'client_id': '',
        'project_id': '',
        'auth_uri': '',
        'token_uri': '',
        'auth_provider_x509_cert_url': '',
        'client_secret': '',
        'redirect_uri': '',
    },
    'database': {
        'filepath': '',
        'username': '',
        'password': '',
    },
    'miscellaneous': {},
}
printer = pprint.PrettyPrinter(indent=4)
log = postr_logger.make_logger('config_parser')

# Internal functions


def _current_config() -> ConfigParser:
    """Gets the current configuration
    Intended to be used internally only
    """
    config = ConfigParser()
    if os.path.isfile(os.path.join(git_root_dir(), CONFIG_FILE)):
        config.read(os.path.join(git_root_dir(), CONFIG_FILE))
    else:
        config.read_dict(DEFAULT_CONFIG)
        _save_config(config)

    return config


def _save_config(config: ConfigParser) -> None:
    """Saves the configuration to a file"""
    with open(os.path.join(git_root_dir(), CONFIG_FILE), 'w') as config_file:
        config.write(config_file)

# Exposes functions to config users


def add_section(section_name: str) -> ConfigParser:
    """Add a new section to the configuration file"""
    config = _current_config()
    config.add_section(section_name)
    _save_config(config)
    return config


def _config_to_dict(config: ConfigParser) -> Mapping[str, Any]:
    """Converts a ConfigParser object to a dictionary
    Used for debugging and printing internally
    """
    dictionary: Mapping[str, Any] = {}
    for section in config.sections():
        dictionary[section] = {}  # type: ignore
        for key, value in config.items(section):
            dictionary[section][key] = value

    return dictionary


def pretty_print_config() -> None:
    """Pretty prints the current config"""
    config = _current_config()
    printer.pprint(_config_to_dict(config))


def update_api_key(api: str, key: str, value: str) -> ConfigParser:
    """Add or update an authentication key for a specified API
    """
    config = _current_config()
    try:
        config[api][key] = value
        _save_config(config)
        log.info(f'Mapping {key} -> {value} added to config for {api}')
    except Exception as exp:
        log.error(f'Failed to add mapping {key} -> {value} to {api}')
        log.error(str(exp))

    return config


def get_api_key(api: str, key: str) -> Optional[str]:
    config = _current_config()
    try:
        return config[api][key]
    except Exception as exp:
        log.error(f'Failed to retrieve {key} from {api}')
        log.error(str(exp))
        return None


def missing_configs_for(api: str) -> List[str]:
    missing_api_keys: List[str] = []
    for key in DEFAULT_CONFIG[api].keys():
        if not get_api_key(api, key) or get_api_key(api, key) == '':
            missing_api_keys.append(key)

    return missing_api_keys


def get_missing_configs() -> Dict[str, Any]:
    missing_configs = {}
    for api, _ in DEFAULT_CONFIG:
        missing_configs[api] = missing_configs_for(api)

    return missing_configs
