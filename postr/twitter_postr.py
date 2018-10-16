# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from typing import Any
from typing import List

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import config

from api_interface import ApiInterface


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def stream_tweets(cls, output_filename: str, hashtags: list) -> None:
        """ Finds realtime tweets given a list of hashtags to look for.
            Writes results to an output file"""
        listener = StdOutListener(output_filename)
        auth = OAuthHandler(get_key('CONSUMER_KEY'), get_key('CONSUMER_SECRET'))
        auth.set_access_token(get_key('ACCESS_TOKEN'), get_key('ACCESS_TOKEN_SECRET'))
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
                tf.write(raw_data)
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
        return True

    @classmethod
    def on_error(cls, status_code: int) -> None:
        """Print an error if the hashtag streaming fails for any reason.
           I can't seem to trigger this function. It probably only gets
           called if the twitter website itself is down. """
        print(status_code)


def get_key(key: str) -> Any:
    """Gets a specified key for the twitter API """
    return config.get_api_key('Twitter', key)


class Twitter(ApiInterface):
    def __init__(self, hashtags: List[str], output_file: str) -> None:
        self.hashtags = hashtags
        self.output_file = output_file

    # pylint: disable=no-self-use, unused-argument
    def post_text(self, text: str) -> bool:
        """ TODO """
        return True

    # pylint: disable=no-self-use, unused-argument
    def post_video(self, url: str, text: str) -> bool:
        """ TODO """
        return True

    # pylint: disable=no-self-use, unused-argument
    def post_photo(self, url: str, text: str) -> bool:
        """ TODO """
        return True

    # pylint: disable=no-self-use, unused-argument
    def get_user_likes(self) -> int:
        """ TODO """
        return -1

    # pylint: disable=no-self-use, unused-argument
    def get_user_followers(self, text: str) -> List[str]:
        """ TODO """
        return [text]

    # pylint: disable=no-self-use, unused-argument
    def remove_post(self, post_id: str) -> bool:
        """ TODO """
        return True

    def stream_tweets_to_output_file(self) -> None:
        twitter_streamer = TwitterStreamer()
        twitter_streamer.stream_tweets(self.output_file, self.hashtags)
