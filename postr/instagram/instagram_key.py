from typing import Any
from ..config import get_api_key


class InstagramKey:
    """ Used to provide easy access to Instagram API keys """

    def __init__(self) -> None:
        """ Stores login info for the user """
        self.username = get_key('USERNAME')
        self.password = get_key('PASSWORD')

        self.pre_profile = get_key('PRE_PROFILE_JSON_URL')
        self.rank_token = get_key('RANK_TOKEN')
        self.post_profile = get_key('POST_PROFILE_JSON_URL')


def get_key(key: str) -> Any:
    """ Gets a specified key for the Instagram API """
    return get_api_key('Instagram', key)
