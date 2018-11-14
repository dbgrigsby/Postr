from typing import List
from typing import Any
from typing import Dict
import json
import urllib
import urllib.request

from InstagramAPI import InstagramAPI

from .instagram.instagram_key import InstagramKey
from .api_interface import ApiInterface


class _InstagramUser:
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

    # A workaround URL that retrieves a profile JSON without triggering a 403 error.
    # URL before the username
    PRE_PROFILE_URL = 'https://www.instagram.com/web/search/topsearch/?context=blended&query='
    # URL after the username, which loads the profile JSON
    POST_PROFILE_URL = '&rank_token=0.3953592318270893&count=1'

    def __init__(self) -> None:
        self.keys = InstagramKey()
        self.api = InstagramAPI(self.keys.username, self.keys.password)
        self.api.login()
        self.uid = self.api.username_id

        self.followers: List[_InstagramUser] = self._user_follower_info()
        self.followings: List[_InstagramUser] = self._user_following_info()

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
        followers: List[_InstagramUser] = self._user_follower_info()
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
        self.followers = self._user_follower_info()
        self.followings = self._user_following_info()

    @staticmethod
    def direct_share(mediaID: str, recipients: List[int], message: str = '') -> None:
        """
        Shares media to a list of recipients via a direct message
        mediaID: The id of the media to share
        recipients: A list of the user ids to share media with
        mesage: The message to go along with the media share
        """
        InstagramAPI.direct_share(mediaID, recipients, message)

    def spam_follower_ratio(self, uid: int = 0) -> float:
        """ Determines the ratio of spam followers on a given user.
            Assumption: A spam account is an account with a default profile
            picture, as well as a 10x or greater following/follower ratio """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        # Get the followers for the given uid
        followers: List[_InstagramUser] = self._user_follower_info(uid)

        # Filter the followers based on default profile picture
        default_profile_followers = list([x for x in followers if not x.is_anon])

        # Filter the followers again based on if the remaining are likely to be spam accounts
        spam_default_profiles = list([x for x in default_profile_followers if self._has_following_ratio_of(x, 10)])

        return len(spam_default_profiles) / len(followers)

    @staticmethod
    def username_to_id(username: str) -> int:
        """
        Converts a username to its associated id

        Unfortunately this isn't built in from the InstagramAPI (they wanted to decrease bot usage)
        so I had to build this myself.

        This function has a small chance of error, as documented in the _username_to_profile() function
        """
        profile_json = Instagram._username_to_profile(username)
        user = Instagram._profile_to_InstagramUser(profile_json)
        return user.uid

    def follow_by_id(self, uid: int) -> None:
        """ Follows a user based off of their uid """
        self.api.follow(uid)

    def unsafe_follow_by_username(self, username: str) -> None:
        """
        Follows a user based off their username
        See the _username_to_profile() function for correctness concerns
        """
        uid = InstagramAPI.username_to_id(username)
        self.api.follow(uid)

    def block_by_id(self, uid: int) -> None:
        """ Blocks a user based off their uid """
        self.api.block(uid)

    def unsafe_block_by_username(self, username: str) -> None:
        """
        Blocks a user based off their username
        Seee the _username_to_profile() function for correctness concerns
        """
        uid = InstagramAPI.username_to_id(username)
        self.api.block(uid)

    @staticmethod
    def _profile_to_InstagramUser(profile: Dict[str, Any]) -> _InstagramUser:
        """ Given a user profile JSON, builds an InstagramUser """
        # Navigate to the user JSON that is coincidentally used by the provided API methods
        user = profile['users'][0]['user']

        # Simply build our InstagramUser, as the user JSON is the same
        return _InstagramUser(user)

    @staticmethod
    def _username_to_profile(username: str) -> Dict[str, Any]:
        """
        Creates a json out of a user's profile info given their username

        If the username contains any special characters, or just by random chance, Instagram
        will not return the correct user. Instead, it seems to return any user whose name is
        relatively similar to the given username. Is this a fuzzy matching error?

        I'm not the first to discover this flaw.
        https://stackoverflow.com/a/13586797

        Hopefully Instagram fixes this flaw.
        """

        base_url = Instagram.PRE_PROFILE_URL + username + Instagram.POST_PROFILE_URL
        print(base_url)

        # Build the page source url for the given user's account
        con = urllib.request.urlopen(base_url)
        user_profile = con.read().decode('utf-8')

        # Convert the webpage to a profile JSON
        profile: dict = json.loads(str(user_profile))
        return profile

    def _has_following_ratio_of(self, user: _InstagramUser, ratio: float) -> bool:
        """ Determines if a user has a following/follower ratio greater than a threshold """
        follower_count = len(self._user_follower_info(uid=user.uid))
        following_count = len(self._user_following_info(uid=user.uid))

        if follower_count == 0:
            return True

        return (following_count / follower_count) > ratio

    def _user_follower_info(self, uid: int = 0) -> List[_InstagramUser]:
        """
        Gets info about followers
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        followers: List[Dict[str, Any]] = self.api.getTotalFollowers(uid)
        user_followers = list([_InstagramUser(x) for x in followers])
        return user_followers

    def _user_following_info(self, uid: int = 0) -> List[_InstagramUser]:
        """
        Gets info about followings
        rtype: List of JSON representing users
        """
        # If no uid was specified, use the authenticated user's uid
        if uid == 0:
            uid = self.uid

        followings: List[Dict[str, Any]] = self.api.getTotalFollowings(uid)
        user_followings = list([_InstagramUser(x) for x in followings])
        return user_followings
