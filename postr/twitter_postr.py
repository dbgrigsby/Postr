# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Variables that contain the user credentials to access the twitter API.
ACCESS_TOKEN: str = '1034473360628039680-OflwYTsKwd6xh1nzcRWje6veoHsBDY'
ACCESS_TOKEN_SECRET: str = '5NqHxFb7ZfwiD07hbSkRq3c9AkyPnOWgnIo4ZUpwjKchZ'
CONSUMER_KEY: str = 'SiPdFBFFoLyVOuThjWMMI0ozI'
CONSUMER_SECRET: str = 'ocg9XwH4FYiz5IZXgxfD3Sowww7UDCSZ8rxLlyLwDvnhuaaHan'


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def stream_tweets(cls, output_filename: str, hashtags: list):
        listener = StdOutListener(output_filename)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hashtags)


class StdOutListener(StreamListener):
    """
    A basic listener for real time hashtags
    """

    def __init__(self, filename: str) -> None:
        self.fetched_tweets_filename = filename
        super().__init__()

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
            return True
        except BaseException as e:
            print('Error on data %s' % str(e))
        return True

    def on_error(self, status_code) -> None:
        print(status_code)


if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ['politics']
    fetched_tweets_filename = 'tweets.txt'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
