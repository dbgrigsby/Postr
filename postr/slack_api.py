import time
from typing import List
import urllib.request
import shutil
import os
from slackclient import SlackClient

from postr.config import get_api_key
from postr.git_tools import git_root_dir
from postr.config import update_api_key
from postr.api_interface import ApiInterface
from postr.postr_logger import make_logger

default_channel = get_api_key('Slack', 'default_channel') or ''
LOG_FOLDER = 'slack'
log = make_logger(LOG_FOLDER)


def download(url: str, extension: str) -> str:
    path = os.path.join(git_root_dir(), 'logs', LOG_FOLDER)
    prefix = 'postr_slack_download'
    timestamp = str(time.time()).replace('.', '_')
    file_name = os.path.join(path, prefix + timestamp + '.' + extension)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        return file_name


def extension_from_url(url: str) -> str:
    return url.split('.')[-1]


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
        # extension = extension_from_url(url)
        return self.post_file(url, text)

    #  def post_file(self, url: str, title: str, extension: str) -> bool:
    def post_file(self, url: str, title: str) -> bool:
        ''' This method takes in the url for the photo the user wants
        to post and returns the success of this action'''
        try:
            # file_name = download(url, extension)
            file_name = url  # Changed to filename at last minute
            log.info(f'File successfully downloaded to {file_name}')
            with open(file_name, 'rb') as file_content:
                self.client.api_call(
                    'files.upload',
                    channels=default_channel,
                    file=file_content,
                    title=title,
                )
            return True
        except Exception as e:
            log.error(f'Failed to post photo with error: {e}')
            return False

    def post_photo(self, url: str, text: str) -> bool:
        # extension = extension_from_url(url)
        return self.post_file(url, text)

    def get_user_likes(self) -> int:
        '''Slack does not support user likes'''
        return -1

    def get_user_followers(self, text: str) -> List[str]:
        '''Slack does not support following a user'''
        return [text]

    def remove_post(self, post_id: str) -> bool:
        channel = default_channel
        result = self.client.api_call('chat.delete', channel=channel, ts=post_id)
        success: bool = result['ok']
        return success


if __name__ == '__main__':
    slack = SlackApi()
    print(slack.post_text('Postr has started!'))
    # print(slack.post_photo(url='http://i.imgur.com/FwDiy5m.png', text='schedule'))
    # print(slack.post_photo(url='http://techslides.com/demos/sample-videos/small.mp4', text='video'))
