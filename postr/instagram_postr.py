from typing import List
from typing import Any
from typing import Dict

from InstagramAPI import InstagramAPI

from .instagram.instagram_key import InstagramKey
from .api_interface import ApiInterface


class Instagram(ApiInterface):
    """ Wrapper for accessing the instagram API  """

    def __init__(self) -> None:
        self.keys = InstagramKey()
        self.api = InstagramAPI(self.keys.username, self.keys.password)
        self.api.login()

    def post_text(self, text: str) -> bool:
        """ Not an operation that this platform has.  """
        return False

    def post_video(self, url: str, text: str) -> bool:
        """ Not an operations that the Instagram API allows. """
        return False

    def post_photo(self, url: str, text: str) -> bool:
        self.api.uploadPhoto(photo=url, caption=text)
        return False

    def get_user_likes(self) -> int:
        """ Not supported by the API """
        return -1

    def get_user_followers(self, text: str) -> List[str]:
        # Get all follower information
        followers: List[Dict[str, Any]] = self.follower_info()
        # Convert each folllower to just their name
        names: List[str] = list(map(lambda x: str(x['username']), followers))
        return names

    def remove_post(self, post_id: str) -> bool:
        try:
            self.api.deleteMedia(mediaId=post_id)
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
            return False

    def follower_info(self) -> List[Dict[str, Any]]:
        """
        Gets info about followers
        rtype: List of JSON representing users
        """
        user_id = self.api.username_id
        followers: List[Dict[str, Any]] = self.api.getTotalFollowers(user_id)
        return followers


if __name__ == '__main__':
    pass
