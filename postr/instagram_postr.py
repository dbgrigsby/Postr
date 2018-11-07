from typing import List
from typing import Any
from typing import Dict

from InstagramAPI import InstagramAPI

from .instagram.instagram_key import InstagramKey
from .api_interface import ApiInterface


class __InstagramUser:
    """ Stores a user defined by the InstagramAPI user JSON """

    def __init__(self, user: Dict[str, Any]) -> None:
        self.uid = int(user['pk'])
        self.username = str(user['username'])
        self.full_name = str(user['full_name'])
        self.profile_pic_url = str(user['profile_pic_url'])

        self.is_private = bool(user['is_private'])
        self.is_verified = bool(user['is_verified'])
        self.is_anon = bool(user['has_anonymous_profile_picture'])


class Instagram(ApiInterface):
    """ Wrapper for accessing the instagram API  """

    def __init__(self) -> None:
        self.keys = InstagramKey()
        self.api = InstagramAPI(self.keys.username, self.keys.password)
        self.api.login()
        self.uid = self.api.username_id

        self.followers: List[__InstagramUser] = self.__user_follower_info()
        self.followings: List[__InstagramUser] = self.__user_following_info()

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
        followers: List[__InstagramUser] = self.__user_follower_info()
        # Convert each folllower to just their name
        names: List[str] = list([x.username for x in followers])
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

    def spam_follower_ratio(self, uid: int = 0) -> float:
        """ Determines the ratio of spam followers on a given user.
            Assumption: A spam account is an account with a default profile
            picture, as well as a 10x or greater following/follower ratio """

        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        # Get the followers for the given uid
        followers: List[__InstagramUser] = self.__user_follower_info(uid)

        # Filter the followers based on default profile picture
        default_profile_followers = list([x for x in followers if not x.is_anon])

        # Filter the followers again based on if the remaining are likely to be spam accounts
        spam_default_profiles = list([x for x in default_profile_followers if self.__has_following_ratio_of(x, 10)])

        return len(spam_default_profiles) / len(followers)

    def __has_following_ratio_of(self, user: __InstagramUser, ratio: float) -> bool:
        """ Determines if a user has a following/follower ratio greater than a threshold """
        follower_count = len(self.__user_follower_info(uid=user.uid))
        following_count = len(self.__user_following_info(uid=user.uid))

        if follower_count == 0:
            return True

        return (following_count / follower_count) > ratio

    def __user_follower_info(self, uid: int = 0) -> List[__InstagramUser]:
        """
        Gets info about followers
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        followers: List[Dict[str, Any]] = self.api.getTotalFollowers(uid)
        user_followers = list([__InstagramUser(x) for x in followers])
        return user_followers

    def __user_following_info(self, uid: int = 0) -> List[__InstagramUser]:
        """
        Gets info about followings
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        followings: List[Dict[str, Any]] = self.api.getTotalFollowings(uid)
        user_followings = list([__InstagramUser(x) for x in followings])
        return user_followings
