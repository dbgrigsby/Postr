# Facebook API
from typing import List

import config
import facebook
import requests
from api_interface import ApiInterface
# import socket
# import sys
# import webbrowser
# import urllib3
# from io import BytesIO
# from http.client import HTTPResponse


class FacebookApi(ApiInterface):

    def __init__(self):
        # fbInfo = config._current_config()['FACEBOOK']
        if(config.get_api_key('FACEBOOK', 'isLoggedIn') == 'true'):
            print('true')
            authToken = config.get_api_key('FACEBOOK', 'authToken')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version='2.12',
            )
        else:
            # need to find way to get facebook auth token val

            # start a socket
            # do a while loop
            # if we get something back, print it
            # if it contains the auth key, store it

            app_id = config.get_api_key('FACEBOOK', 'appId')
            canvas_url = 'https://www.facebook.com/connect/login_success.html'
            # 'https://127.0.0.1:8888'
            # "https://domain.com/that-handles-auth-response/"
            perms = ['manage_pages', 'publish_pages']
            # perms = []
            token = config.get_api_key('FACEBOOK', 'appToken')
            test = facebook.GraphAPI(access_token=token, version='2.12')
            url = test.get_auth_url(app_id, canvas_url, perms)
            print(url)

            # webbrowser.open(fb_login_url)
            r = requests.get(url)
            # to set auth token, we need to ask user for permission
            # url = http://127.0.0.1:8888do i need port?
            print('about to print the damn thing')

            print(r.url)
            print(r.history[0].url)
            print(r.history[1].content)

            val = 'testing'
            # config.update_api_key('FACEBOOK', 'isLoggedIn', 'true')
            config.update_api_key('FACEBOOK', 'authToken', val)

            # create graph for user
            authToken = config.get_api_key('FACEBOOK', 'authToken')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version="2.12",
            )

    def postText(s: str) -> bool:
        # self.graph.put_object(parent_object='me', connection_name='feed',
        # message=s)
        return True

    def postVideo(url: str, text: str) -> bool:
        # self.graph.put_object(
        # parent_object="me",
        # connection_name="feed",
        # message=text,
        # link=url)
        return True

    def postPhoto(url: str, text: str) -> bool:
        # self.graph.put_photo(image=open(url, 'rb'), message=text)
        return True

    def getUserLikes() -> int:
        # self.graph.get_connections(id='me', connection_name='friends')
        return 0

    def getUserFollowers(stringTxt: str) -> List[str]:
        # self.graph.get_connections(id='me', connection_name='friends')
        return None

    def removePost(postId: str) -> bool:
        # self.graph.delete_object(id=postId)
        return True


test = FacebookApi()
