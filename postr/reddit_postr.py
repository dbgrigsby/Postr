from typing import Any

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


def submit_subreddit_post() -> None:
    subreddit = reddit_refresh.subreddit('Postr')
    subreddit.submit('Postr_Test', url='https://github.com/dbgrigsby/Postr/')


def get_reddit_refresh_token(authorized_code: str) -> Any:
    """
    Utilizes the code gained from a user approving
    the application through the link found from get_reddit_oauth.
    After utilization, returns refresh token and discards
    authorized_code to disallow future use.
    """
    return reddit.auth.authorize(authorized_code)


reddit_refresh = praw.Reddit(
    user_agent='Postr (by Adam Beck, Dan Grisby, Tommy Lu, Dominique Owens, Rachel Pavlakovic)',
    client_id='AZQxN0WW9txW3g', client_secret=None,
    refresh_token='175172957565-NI61KRGDJaLIaez4MGv4mY9SIPo',
)

print(reddit_refresh.auth.scopes())
submit_subreddit_post()
