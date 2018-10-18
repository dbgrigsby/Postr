import json
import time
from typing import List

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API
from tweepy.streaming import StreamListener
from tweepy.cursor import Cursor

from api_interface import ApiInterface
from twitter_key import TwitterKey
from twitter_info import TwitterInfo


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def __init__(self, keys: TwitterKey) -> None:
        """ Holds API keys for twitter access """
        self.keys = keys

    @staticmethod
    def stream_tweets(hashtags: List[str], output_filename: str, auth: OAuthHandler) -> None:
        """ Finds realtime tweets given a list of hashtags to look for.
            Writes results to an output file"""
        listener = StdOutListener(output_filename)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hashtags)


class StdOutListener(StreamListener):
    """ A basic listener for real time hashtags """

    def __init__(self, filename: str) -> None:
        """Constructor for the realtime streaming, writes results to the filename output file"""
        self.fetched_tweets_filename = filename
        super().__init__()

    def on_data(self, raw_data: str) -> bool:
        """Writes a tweet and all associated info that was streamed to an output file """
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                j = json.loads(raw_data)
                tf.write(j['text'])
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
        return True

    @staticmethod
    def on_error(status_code: int) -> None:
        """Print an error if the hashtag streaming fails for any reason.
           I can't seem to trigger this function. It probably only gets
           called if the twitter website itself is down. """
        print(status_code)


class Twitter(ApiInterface):
    def __init__(self) -> None:
        """ Store easy access for keys """
        self.keys = TwitterKey()

        """ Store pointer for OAuth access """
        auth = OAuthHandler(self.keys.consumer_pub, self.keys.consumer_sec)
        auth.set_access_token(self.keys.access_pub, self.keys.access_sec)
        self.auth = auth
        self.api = API(auth)

        """ Store easy access for twitter info operations """
        self.info = TwitterInfo(self.api)

    def post_text(self, text: str) -> bool:
        """ Posts a tweet containing text """
        try:
            self.api.update_status(status=text)
            return True
        except BaseException as e:
            print(e)
            return False

    # pylint: disable=no-self-use, unused-argument
    def post_video(self, url: str, text: str) -> bool:
        """ Not applicable """
        return False

    def post_photo(self, url: str, text: str) -> bool:
        """ Posts a tweet with text and a picture """
        try:
            self.api.update_with_media(filename=url, status=text)
            return True
        except BaseException as e:
            print(e)
            return False

    def get_user_followers(self, text: str) -> List[str]:
        """ Gets user followers, note: this is rate limited """
        my_followers = []
        i = 0

        # Use the cursor module for pagination
        for follower in Cursor(self.api.followers, screen_name=text).items():
            my_followers.append(follower.screen_name)
            i += 1

            # Simple rate limit for requests
            if i >= 100:
                i = 0
                time.sleep(1)

        return my_followers

    def remove_post(self, post_id: str) -> bool:
        """ Removes a tweet given its ID """
        try:
            self.api.destroy_status(post_id)
            return True
        except BaseException as e:
            print(e)
            return False

    def stream_tweets(self, hashtags: List[str], output_filename: str) -> None:
        """ Streams tweets from a hashtag and writes data into an output file """
        twitter_streamer = TwitterStreamer(self.keys)
        twitter_streamer.stream_tweets(hashtags, output_filename, self.auth)

    # pylint: disable=no-self-use, unused-argument
    def get_user_likes(self) -> int:
        """ Not applicable, see helper methods in TwitterInfo class"""
        return -1


if __name__ == '__main__':
    t = Twitter()
    t.post_text('sample API post')
