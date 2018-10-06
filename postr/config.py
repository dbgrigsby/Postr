import logging
import os.path
import pprint
from configparser import ConfigParser
from typing import Any
from typing import Mapping
from typing import Optional

import git

# Creates or reads the authentication config file
CONFIG_FILE = 'postr_config.ini'
DEFAULT_CONFIG: Mapping[str, Mapping[str, Any]] = {
    'Discord': {
        'client_secret': '',
    },
    'Facebook': {},
    'Twitter': {},
    'Reddit': {},
    'Slack': {},
    'Instagram': {},
    'Tumblr': {},
    'YouTube': {},
    'database': {
        'filepath': '',
        'username': '',
        'password': '',
    },
    'miscellaneous': {},
}
printer = pprint.PrettyPrinter(indent=4)

# Internal functions


def _git_root_dir() -> str:
    git_repo = git.Repo('.', search_parent_directories=True)
    git_root = git_repo.git.rev_parse('--show-toplevel')
    return str(git_root)


def _current_config() -> ConfigParser:
    """Gets the current configuration
    Intended to be used internally only
    """
    config = ConfigParser()
    if os.path.isfile(os.path.join(_git_root_dir(), CONFIG_FILE)):
        config.read(os.path.join(_git_root_dir(), CONFIG_FILE))
    else:
        config.read_dict(DEFAULT_CONFIG)
        _save_config(config)

    return config


def _save_config(config: ConfigParser) -> None:
    """Saves the configuration to a file"""
    with open(os.path.join(_git_root_dir(), CONFIG_FILE), 'w') as config_file:
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
        logging.info(f'Mapping {key} -> {value} added to config for {api}')
    except Exception as exp:
        logging.error(f'Failed to add mapping {key} -> {value} to {api}')
        logging.error(str(exp))

    return config


def get_api_key(api: str, key: str) -> Optional[str]:
    config = _current_config()
    try:
        return config[api][key]
    except Exception as exp:
        logging.error(f'Failed to retrieve {key} from {api}')
        logging.error(str(exp))
        return None
