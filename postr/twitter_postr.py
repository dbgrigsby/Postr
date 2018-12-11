import csv
import datetime
import json
import re
import os
import time
from typing import List

import matplotlib
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.api import API
from tweepy.streaming import StreamListener
from tweepy.cursor import Cursor
from textblob import TextBlob

from .api_interface import ApiInterface
from .twitter.twitter_key import TwitterKey
from .twitter.twitter_info import TwitterInfo
from .twitter.twitter_bio import TwitterBio


matplotlib.use('TkAgg')
# Precision to truncate on a datetime object, down to the minute
DATETIME_MILLISECOND_PRECISION = 23

# Precision to truncate scores when plotting twitter stream scores
SCORE_PRECISION = 5


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def __init__(self, keys: TwitterKey, graphfile: str) -> None:
        """ Holds API keys for twitter access """
        self.keys = keys
        self.graphfile = graphfile

    def stream_tweets(self, hashtags: List[str], output_filename: str, auth: OAuthHandler) -> None:
        """ Finds realtime tweets given a list of hashtags to look for.
            Writes results to an output file"""
        listener = StdOutListener(output_filename, self.graphfile)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hashtags)


class StdOutListener(StreamListener):
    """ A basic listener for real time hashtags """

    def __init__(self, filename: str, graphfile: str) -> None:
        """Constructor for the realtime streaming, writes results to the filename output file"""
        self.fetched_tweets_filename = filename
        self.graphfile = graphfile
        self.counter = 0
        super().__init__()

    def on_data(self, raw_data: str) -> bool:
        """Writes a tweet and all associated info that was streamed to an output file """
        try:
            if self.counter == 10:
                return False
            print('found tweet #%d' % self.counter)

            with open(self.fetched_tweets_filename, 'a') as tf:
                j = json.loads(raw_data)
                tf.write(j['text'])

            with open(self.graphfile, 'a') as gf:
                writer = csv.writer(gf)
                writer.writerow([j['text'], datetime.datetime.now()])

            self.counter += 1
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
        self.bio = TwitterBio(self.api)

        """ Contains info for real-time graphing """
        self.streamfile = os.path.join('postr', 'twitter', 'twitter_stream.txt')
        self.graphfile = os.path.join('postr', 'twitter', 'twitter_graphing.csv')
        self.blobfile = os.path.join('postr', 'twitter', 'twitter_blob.csv')

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
        self.setup_csv()
        twitter_streamer = TwitterStreamer(self.keys, self.graphfile)
        twitter_streamer.stream_tweets(hashtags, output_filename, self.auth)
        print('done streaming')

    def setup_csv(self) -> None:
        """ Initializes a csv file for time series graphing """
        csvData = ['Tweet', 'Time']

        with open(self.graphfile, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
            csvFile.close()

    # pylint: disable=no-self-use, unused-argument
    def get_user_likes(self) -> int:
        """ Not applicable, see helper methods in TwitterInfo class"""
        return -1

    def read_csv_col(self, colNum: int, filename: str) -> List[str]:
        """ Reads a specific column by index in the graph csv"""
        col = []
        with open(filename, 'r') as rf:
            reader = csv.reader(rf, delimiter=',')
            for row in reader:
                col.append(str(row[colNum]))

        return col[1::]  # Ignore the csv header

    def analyzeSentiment(self) -> None:
        """ Converts a real-time tweet content into a positivity score"""
        with open(self.blobfile, 'w') as bf:
            writer = csv.writer(bf)
            graph_data = zip(
                self.read_csv_col(0, self.graphfile),
                self.read_csv_col(1, self.graphfile),
            )

            for pair in graph_data:
                text = str(re.sub(r'[^a-zA-Z ]+', '', pair[0]))
                score = Twitter.polarity(text)
                writer.writerow([pair[1], score])

            bf.close()

    @staticmethod
    def polarity(text: str) -> float:
        """ Returns the polarity of text. Made into a separate
            method to provide easy modification if needed in the future """
        return float(TextBlob(text).sentiment.polarity)

    def stream_and_graph(self, hashtags: List[str]) -> None:
        """ Streams tweets in real time, then graphs their sentiment """
        self.stream_tweets(hashtags, self.streamfile)
        self.analyzeSentiment()
        self.graph_blob()

    def graph_blob(self) -> None:
        """ Graphs a blob file for twitter sentiment """
        dates = self.read_csv_col(0, self.blobfile)
        # Truncate the datetime object to the minute precision
        dates = [d[:DATETIME_MILLISECOND_PRECISION] for d in dates]

        # Truncate off scores past a precision for easy viewing on the plot
        scores = list(map(lambda x: x[:SCORE_PRECISION], self.read_csv_col(1, self.blobfile)))

        plt.plot(
            dates,
            scores,
        )

        plt.ylabel('Positivity Score')
        plt.xlabel('Time')

        # beautify the x-labels
        plt.gcf().autofmt_xdate()

        plt.show()

    def update_bio(self, message: str) -> None:
        """ Sets an authenticated user's bio to a specified message """
        self.api.update_profile(description=message)


def examples() -> None:
    """ Runs through major use cases """
    t = Twitter()

    # text and picture posting
    t.post_text('sample API text')
    # t.post_photo('enter path here', 'sample API text'), put a valid path here to use

    # Get/Set info about the authenticated user
    print(t.bio.username())
    print(t.bio.bio())
    t.update_bio('sample API bio')
    t.bio.update_name('Postr Project')

    # Get info about the authenticated user's tweets
    twt = t.info.last_tweet()  # Returns a Status object. Let's use it.
    # All methods for a Status object:: https://gist.github.com/dev-techmoe/ef676cdd03ac47ac503e856282077bf2
    print(twt.text)
    print(twt.retweet_count)
    print(twt.favorite_count)

    # Let's stream some hashtags and graph them in real time
    t.stream_and_graph(['Politics', 'News', 'School'])


if __name__ == '__main__':
    examples()
