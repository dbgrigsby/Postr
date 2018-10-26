from typing import List
from api_interface import ApiInterface


# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class Youtube(ApiInterface):

    def __init__(self) -> None:
        pass
        # TODO placeholder config
        # self.flow = InstalledAppFlow.from_client_config(google_secret)
        # auth_url, _ = self.flow.authorization_url(prompt='consent')
        # print(auth_url)

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        return True

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        return True

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        return True

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has total between link and client'''
        return 0

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        # Not possible on reddit, someone who friends someone is one-way and private.
        # This is due to the fact that any public reddit posts are public from a user,
        # and becoming friends only involves seeing someone's posts on a separate tab.
        # This is why the pylint precommit is disabled

        # pylint: disable=unused-argument
        # pylint: disable=R0201
        return None  # type: ignore

    def remove_post(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the success of this action'''
        # TODO failure checking
        return True


# def get_key(key: str) -> Any:
#    """Gets a specified key for the reddit API """
#    return config.get_api_key('Reddit', key)

new_Youtube = Youtube()
