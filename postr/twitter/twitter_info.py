from tweepy.api import API
from tweepy.models import Status


class TwitterInfo():
    """
    Class for obtaining info about twitter related operations
    """

    def __init__(self, api: API) -> None:
        """ Holds API keys for twitter access """
        self.api = api

    def id(self) -> int:
        """ Gets the id of the authenticated user """
        return int(self.api.me().id)

    def last_tweet(self) -> Status:
        """ Returns the info of the authenticated user's latest tweet """
        return self.api.user_timeline(id=self.id(), count=1)[0]

    def latest_favorites(self) -> int:
        """ Returns the favorite count of the latest tweet """
        return self.favorites_on(self.last_tweet().id)

    def favorites_on(self, tweet_id: int) -> int:
        """ Returns the favorite count of a specified tweet """
        return int(self.api.get_status(tweet_id).favorite_count)

    def latest_retweets(self) -> int:
        """ Returns the retweet count of the latest tweet """
        return self.retweets_on(self.last_tweet().id)

    def retweets_on(self, tweet_id: int) -> int:
        """ Returns the retweet count of a specified tweet """
