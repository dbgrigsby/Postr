from typing import Any
import config


class TwitterKey:
    """ Used to provide easy access to twitter APi keys"""

    def __init__(self) -> None:
        """ Stores the consume and access public and private keys """
        self.consumer_pub = get_key('CONSUMER_KEY')
        self.consumer_sec = get_key('CONSUMER_SECRET')
        self.access_pub = get_key('ACCESS_TOKEN')
        self.access_sec = get_key('ACCESS_TOKEN_SECRET')


def get_key(key: str) -> Any:
    """ Gets a specified key for the twitter API """
    return config.get_api_key('Twitter', key)
