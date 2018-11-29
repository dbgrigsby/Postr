import csv
import datetime
from typing import List
from typing import Any
from typing import Dict
from typing import Tuple
import json
import os
import urllib
import urllib.request

import matplotlib.pyplot as plt
from InstagramAPI import InstagramAPI

from .instagram.instagram_key import InstagramKey
from .api_interface import ApiInterface

# Precision to truncate on a datetime object, down to the minute
DATETIME_MINUTE_PRECISION = 16


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

    def __init__(self) -> None:
        # Store keys and api info
        self.keys = InstagramKey()
        self.api = InstagramAPI(self.keys.username, self.keys.password)
        self.api.login()

        # Store the authenticated user's Instagram UID
        self.uid = self.api.username_id

        # Memoize follower and following information for the authenticated user
        self.followers: List[_InstagramUser] = self._user_follower_info()
        self.followings: List[_InstagramUser] = self._user_following_info()

        # Specify the output graphfile for follower/time graphing
        self.graphfile = os.path.join('postr', 'instagram', 'instagram_graphing.csv')

        if not os.path.isfile(self.graphfile):
            self.setup_csv()

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
    def direct_share(media_id: str, recipients: List[int], message: str = '') -> None:
        """
        Shares media to a list of recipients via a direct message
        mediaID: The id of the media to share
        recipients: A list of the user ids to share media with
        mesage: The message to go along with the media share
        """
        InstagramAPI.direct_share(media_id, recipients, message)

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

    def username_to_id(self, username: str) -> int:
        """
        Converts a username to its associated id

        Unfortunately this isn't built in from the InstagramAPI (they wanted to decrease bot usage)
        so I had to build this myself.

        This function has a small chance of error, as documented in the _username_to_profile() function
        """
        profile_json = self._username_to_profile(username)
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
        uid = self.username_to_id(username)
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

    def setup_csv(self) -> None:
        """ Initializes a csv file for the time series graphing """
        csvData = ['Followers', 'Time']

        # Create our CSV file header
        with open(self.graphfile, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
            csvFile.close()

    def log_followers(self) -> None:
        """ Logs follower information to the graph file """
        with open(self.graphfile, 'a') as gf:
            writer = csv.writer(gf)
            follower_count = len(self.get_user_followers(''))
            date = datetime.datetime.now()

            # Append the current date and follower count to the file
            writer.writerow([date, follower_count])
            gf.close()

    @staticmethod
    def _read_csv_col(colNum: int, filename: str) -> List[str]:
        """ Reads a specific column by index in the graph csv"""
        col = []
        with open(filename, 'r') as rf:
            reader = csv.reader(rf, delimiter=',')
            for row in reader:
                col.append(str(row[colNum]))

        return col[1::]  # Ignore the csv header

    def graph_followers(self) -> None:
        """ Graphs a blob file for twitter sentiment """

        def max_followers(followers: List[int]) -> Tuple[int, int]:
            """ Finds the max followers with its index, for global maxima plotting """
            max_val = 0
            max_index = 0
            for index, val in enumerate(followers):
                if val > max_val:
                    max_val = val
                    max_index = index
            return (max_index, max_val)

        # plot
        dates = Instagram._read_csv_col(0, self.graphfile)

        # Truncate the datetime object to the minute precision
        dates = [d[:DATETIME_MINUTE_PRECISION] for d in dates]
        scores = Instagram._read_csv_col(1, self.graphfile)

        (max_index, max_val) = max_followers([int(s) for s in scores])

        plt.plot(
            dates,
            scores,
        )

        plt.ylabel('Follower count')
        plt.xlabel('Time')

        # Annotate the plot with the global max
        plt.annotate(
            'Absolute max', xy=(max_index, max_val - 1),
            xytext=(max_index, max_val), arrowprops=dict(facecolor='black', shrink=0.05),
        )

        # beautify the x-labels
        plt.gcf().autofmt_xdate()

        # Set our y-range to be the max value plus a few more, to show the annotation
        plt.ylim(-1, max_val + 3)
        plt.show()

    @staticmethod
    def _profile_to_InstagramUser(profile: Dict[str, Any]) -> _InstagramUser:
        """ Given a user profile JSON, builds an InstagramUser """
        # Navigate to the user JSON that is coincidentally used by the provided API methods
        user = profile['users'][0]['user']

        # Simply build our InstagramUser, as the user JSON is the same
        return _InstagramUser(user)

    def _username_to_profile(self, username: str) -> Dict[str, Any]:
        """
        Creates a json out of a user's profile info given their username

        If the username contains any special characters, or just by random chance, Instagram
        will not return the correct user. Instead, it seems to return any user whose name is
        relatively similar to the given username. Is this a fuzzy matching error?

        I'm not the first to discover this flaw.
        https://stackoverflow.com/a/13586797

        Hopefully Instagram fixes this flaw.
        """

        base_url = self.keys.pre_profile + username + self.keys.rank_token + self.keys.post_profile

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

    def example_graphing(self) -> None:
        """ Example method demonstrating graphing """
        # Log the current amount of followers to our history of followers
        self.log_followers()

        # Graphs all followers / time
        self.graph_followers()
