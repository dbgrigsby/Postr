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

        self.followers: List[Dict[str, Any]] = self.__user_follower_info()
        self.followings: List[Dict[str, Any]] = self.__user_following_info()

    def post_text(self, text: str) -> bool:
        """ Not an operation that this platform has. """
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
        """ Gets the names of all users followers """
        # Get all follower information
        followers: List[Dict[str, Any]] = self.__user_follower_info()
        # Convert each folllower to just their name
        names: List[str] = list(map(lambda x: str(x['username']), followers))
        return names

    def remove_post(self, post_id: str) -> bool:
        """ Removes a post, prints an exception if the post doesn't exist """
        try:
            self.api.deleteMedia(mediaId=post_id)
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
            return False

    def refresh(self) -> None:
        """ Updates the stored contents for a user's followers and followings """
        self.followers = self.__user_follower_info()
        self.followings = self.__user_following_info()

    def __user_follower_info(self, uid: int = 0) -> List[Dict[str, Any]]:
        """
        Gets info about followers
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.api.username_id

        followers: List[Dict[str, Any]] = self.api.getTotalFollowers(uid)
        return followers

    def __user_following_info(self, uid: int = 0) -> List[Dict[str, Any]]:
        """
        Gets info about followings
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.api.username_id

        followers: List[Dict[str, Any]] = self.api.getTotalFollowings(uid)
        return followers

    def spam_follower_ratio(self, uid: int = 0) -> float:
        """ Determines the ratio of spam followers on a given user.
            Assumption: A spam account is an account with a default profile
            picture, as well as a 10x or greater following/follower ratio """
        # followers: List[Dict[str, Any]] = self.user_follower_info(uid)
        pass


class __InstagramUser:

    def __init__(self, user: Dict[str, Any]) -> None:
        self.username = str(user['username'])
        self.full_name = str(user['full_name'])
        self.profile_pic_url = str(user['profile_pic_url'])

        self.is_private = bool(user['is_private'])
        self.is_verified = bool(user['is_verified'])
        self.is_anon = bool(user['has_anonymous_profile_picture'])


if __name__ == '__main__':
    pass
