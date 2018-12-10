from urllib.parse import parse_qsl
from typing import List
import oauth2
import pytumblr
from postr.config import get_api_key
from postr.config import update_api_key
from postr.api_interface import ApiInterface


class TumblrApi(ApiInterface):

    def __init__(self) -> None:

        TumblrApi.authenticate()

        consumer_key = get_api_key('Tumblr', 'consumer_key')
        consumer_secret = get_api_key('Tumblr', 'consumer_secret')
        auth_token = get_api_key('Tumblr', 'auth_token')
        auth_token_secret = get_api_key('Tumblr', 'auth_token_secret')

        self.client = pytumblr.TumblrRestClient(
            consumer_key,
            consumer_secret,
            auth_token,
            auth_token_secret,
        )

        info = self.client.info()

        self.blogs: dict = {}
        self.current_blog_name = ''

        if 'blogs' in info:
            # get a list of all blog names
            self.blogs = info['blogs']

            # set first blog name to blog_name
            self.current_blog_name = self.blogs[0].name

    def change_current_blog(self, new_blog_name: str) -> None:
        for blog in self.blogs:
            if blog.name == new_blog_name:
                self.current_blog_name = new_blog_name

    @staticmethod
    def authenticate() -> bool:
        success = True

        try:
            # get all values needed for auth
            consumer_key = get_api_key('Tumblr', 'consumer_key')
            consumer_secret = get_api_key('Tumblr', 'consumer_secret')
            request_token_url = get_api_key('Tumblr', 'request_token_url')

            consumer = oauth2.Consumer(consumer_key, consumer_secret)
            client = oauth2.Client(consumer)

            content = client.request(request_token_url, 'GET')

            request_token = dict(parse_qsl(content))

            OAUTH_TOKEN = request_token[b'oauth_token']
            OAUTH_TOKEN_SECRET = request_token[b'oauth_token_secret']

            update_api_key('Tumblr', 'auth_token', OAUTH_TOKEN)
            update_api_key('Tumblr', 'auth_token_secret', OAUTH_TOKEN_SECRET)

        except Exception:
            success = False

        return success

    def post_text(self, text: str) -> bool:
        success = True
        try:
            self.client.create_text(self.current_blog_name, state='published', body=text)
        except Exception:
            success = False

        return success

    def post_video(self, url: str, text: str) -> bool:
        success = True
        try:
            if ('https' in url) or ('http' in url) or ('.com' in url):
                # Creating an upload from YouTube
                self.client.create_video(self.current_blog_name, caption=text, embed=url)
            else:
                # Creating a video post from local file
                self.client.create_video(self.current_blog_name, caption=text, data=url)
        except Exception:
            success = False

        return success

    def post_photo(self, url: str, text: str) -> bool:

        success = True
        try:
            if ('https' in url) or ('http' in url) or ('.com' in url):
                # Creates a photo post using a source URL
                self.client.create_photo(self.current_blog_name, state='published', caption=text, source=url)
            else:
                # Creates a photo post using a local filepath
                self.client.create_photo(self.current_blog_name, state='published', caption=text, data=url)

        except Exception:
            success = False

        return success

    def get_user_likes(self) -> int:
        like_num = 0
        try:
            like_list = list(self.client.blog_likes(self.current_blog_name))  # get the likes on a blog
            like_num = len(like_list)
        except Exception:
            like_num = -1

        return like_num

    def get_user_followers(self, text: str) -> List[str]:
        try:
            follow_list = list(self.client.followers(self.current_blog_name))
        except Exception:
            follow_list = [text]
        return follow_list

    def remove_post(self, post_id: str) -> bool:
        success = True
        try:
            self.client.delete_post(self.current_blog_name, post_id)
        except Exception:
            success = False

        return success
