from typing import List
from slackclient import SlackClient

from postr.config import get_api_key
from postr.config import update_api_key
from postr.api_interface import ApiInterface

default_channel = get_api_key('Slack', 'default_channel') or ''


class SlackApi(ApiInterface):

    def __init__(self) -> None:
        slack_token = get_api_key('Slack', 'API_TOKEN')
        self.client = SlackClient(slack_token)

    def post_text(self, text: str) -> bool:
        channel = default_channel
        result = self.client.api_call('chat.postMessage', channel=channel, text=text)
        success: bool = result['ok']
        return success

    @classmethod
    def change_default_channel(cls, channel: str) -> None:
        if channel != get_api_key('Slack', 'default_channel'):
            update_api_key('Slack', 'default_channel', channel)
            global default_channel  # pylint: disable=global-statement
            default_channel = channel

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user want to post and returns the success of this action'''
        return False

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user wants
        to post and returns the success of this action'''
        return False

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has'''
        return -1

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that follow the user'''
        return [text]

    def remove_post(self, post_id: str) -> bool:
        channel = default_channel
        result = self.client.api_call('chat.delete', channel=channel, ts=post_id)
        success: bool = result['ok']
        return success


if __name__ == '__main__':
    slack = SlackApi()
    print(slack.post_text('bot started'))
