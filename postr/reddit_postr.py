from typing import List, Any
from api_interface import ApiInterface
import config
import praw

# Scopes for user authentication
# See get_reddit_oauth
# and https://github.com/reddit-archive/reddit/wiki/OAuth2
scopes = {
    'identity',
    'edit',
    'flair',
    'history',
    'modconfig',
    'modflair',
    'modlog',
    'modposts',
    'modwiki',
    'mysubreddits',
    'privatemessages',
    'read',
    'report',
    'save',
    'submit',
    'subscribe',
    'vote',
    'wikiedit',
    'wikiread',
}


class Reddit(ApiInterface):

    def __init__(self) -> None:
        # TODO config for client id, and refresh token
        self.client = praw.Reddit(
            user_agent='Postr (by Adam Beck, Dan Grisby, Tommy Lu, Dominique Owens, Rachel Pavlakovic)',
            client_id=get_key('client_id'), client_secret=None,
            refresh_token=get_key('refresh_token'),
        )
        self.subreddit_name = 'Postr'

    def set_subreddit_name(self, subreddit_name: str) -> bool:
        ''' This method sets the subreddit that the user will post to
        and returns the success of this action'''
        self.subreddit_name = subreddit_name
        return True

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        # TODO set title to something other than first 20 characters of text
        subreddit = self.client.subreddit('Postr')
        subreddit.submit(text[0:20], selftext=text)
        return True

    def post_link(self, url: str, text: str) -> bool:
        ''' This method takes in the simple link the user want to post
        and returns the success of this action'''
        # TODO set_subreddit should add subreddit to config.
        subreddit = self.client.subreddit('Postr')
        subreddit.submit(text, url=url)
        return True

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        # TODO differentiate between YouTube video and image handling site if needed.
        self.post_link(url, text)
        return True

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        self.post_link(url, text)
        return True

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has total between link and client'''
        return int(
            self.client.user.me().comment_karma +
            self.client.user.me().link_karma,
        )

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        # Not possible on reddit, someone who friends someone is one-way and private.
        # This is due to the fact that any public reddit posts are public from a user,
        # and becoming friends only involves seeing someone's posts on a separate tab.
        # This is why the pylint precommit is disabled

        # pylint: disable=unused-argument
        # pylint: disable=R0201
        return None  # type: ignore

    def remove_post(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the successs of this action'''
        # TODO failure checking
        submission = self.client.submission(post_id)
        submission.delete()
        return True

    def remove_comment(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the successs of this action'''
        # TODO failure checking
        comment = self.client.comment(post_id)
        comment.delete()
        return True

    def top_submissions_in_subreddit(self, subreddit_name: str) -> List:
        subreddit = self.client.subreddit(subreddit_name)
        submission_list = []
        for submission in subreddit.hot(limit=25):
            submission_list.append(submission)
        return submission_list


def get_key(key: str) -> Any:
    """Gets a specified key for the reddit API """
    return config.get_api_key('Reddit', key)
