from typing import List
from typing import Any

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API
from tweepy.streaming import StreamListener

from api_interface import ApiInterface
from twitter_key import TwitterKey


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
                tf.write(raw_data)
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
        self.keys = TwitterKey()

        auth = OAuthHandler(self.keys.consumer_pub, self.keys.consumer_sec)
        auth.set_access_token(self.keys.access_pub, self.keys.access_sec)
        self.auth = auth
        self.api = API(auth)

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
        """ Not supported by the api  """
        return False

    def post_photo(self, url: str, text: str) -> bool:
        """ Posts a tweet with text and a picture """
        try:
            self.api.update_with_media(filename=url, status=text)
            return True
        except BaseException as e:
            print(e)
            return False

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

    def stream_tweets_to_output_file(self, hashtags: List[str], output_filename: str) -> None:
        """ Streams tweets from a hashtag and writes data into an output file """
        twitter_streamer = TwitterStreamer(self.keys)
        twitter_streamer.stream_tweets(hashtags, output_filename, self.auth)

    def get_self_status(self, handle: str) -> Any:
        return self.api.get_status()

    def update_bio(self, message: str) -> None:
        self.api.update_profile(description=message)

    def update_name(self, new_name: str) -> None:
        self.api.update_profile(name=new_name)


if __name__ == '__main__':
    t = Twitter()
    t.update_name('test API new name')
