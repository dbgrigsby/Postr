from typing import Any
from ..config import get_api_key


class TwitterKey:
    """ Used to provide easy access to Instagram API keys """

    def __init__(self) -> None:
        """ Stores login info for the user """
        self.username = get_key('USERNAME')
        self.password = get_key('PASSWORD')


def get_key(key: str) -> Any:
    """ Gets a specified key for the Instagram API """
    return get_api_key('Instagram', key)
