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
            client_id='AZQxN0WW9txW3g', client_secret=None,
            refresh_token='175172957565-NI61KRGDJaLIaez4MGv4mY9SIPo',
        )
        self.subreddit = 'Postr'

    def set_subreddit(self, subreddit: str) -> bool:
        ''' This method sets the subreddit that the user will post to
        and returns the success of this action'''
        self.subreddit = subreddit
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
        return -1  # self.client.user.me.comment_karma + self.client.user.me.link_karma

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        # Not possible on reddit, someone who friends someone is one-way and private.
        # This is due to the fact that any public reddit posts are public from a user,
        # and becoming friends only involves seeing someone's posts on a separate tab.
        return []

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


def get_key(key: str) -> Any:
    """Gets a specified key for the reddit API """
    return config.get_api_key('Reddit', key)


reddit = praw.Reddit(
    user_agent='Postr (by Adam Beck, Dan Grisby, Tommy Lu, Dominique Owens, Rachel Pavlakovic)',
    client_id=config.DEFAULT_CONFIG, client_secret=None,
    redirect_uri='https://github.com/dbgrigsby/Postr/',
)


def get_reddit_oauth() -> Any:
    # Note that once a user requests this,
    # the user will be redirected and in the url the code for authorize
    # is in the code = of the url.
    # Will need to explain or get the code token much more easily somehow.
    return reddit.auth.url(
        scopes,
        'https://github.com/dbgrigsby/Postr/',
        'permanent',
    )


def get_reddit_refresh_token(authorized_code: str) -> Any:
    """
    Utilizes the code gained from a user approving
    the application through the link found from get_reddit_oauth.
    After utilization, returns refresh token and discards
    authorized_code to disallow future use.
    """
    return reddit.auth.authorize(authorized_code)
