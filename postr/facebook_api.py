# Facebook API

from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import json
from typing import Type, List
from postr.config import get_api_key
from postr.config import update_api_key
from postr.api_interface import ApiInterface
import facebook


code = ''


class Handler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        request_path = self.path
        global code  # pylint: disable=global-statement
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        code = request_path
        output = '<html><head><title>Postr Facebook Auth</title></head>'
        output += '<body><h1>Thanks For Authenticating with Postr!</h1>'
        output += '<p>You can close this tab.</p>'
        output += '</body></html>'
        self.wfile.write(output.encode())


class Server(HTTPServer):
    pass


class FacebookApi(ApiInterface):

    def __init__(self) -> None:
        success = FacebookApi.authenticate()

        if success:
            authToken = get_api_key('FACEBOOK', 'authToken')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version='2.12',
            )
        else:
            self.graph = facebook.GraphAPI()

    @staticmethod
    def wait_for_request(
        server_class: Type[HTTPServer],
        handler_class: Type[BaseHTTPRequestHandler],
    ) -> None:
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        httpd.timeout = 10
        try:
            httpd.handle_request()  # this can get me the code !!!!
        except KeyboardInterrupt:
            pass
        httpd.server_close()

    @staticmethod
    def parse_code(code_str: str) -> str:
        end = len(code_str)
        # get index of =
        equals_index = code_str.find('=')
        actual_code = code_str[equals_index + 1: end]
        return actual_code

    @staticmethod
    def extract_access_token(dic: dict) -> str:
        return str(dic['access_token'])

    @staticmethod
    def authenticate() -> bool:
        success = True
        try:
            # get all values needed for auth
            app_id = get_api_key('FACEBOOK', 'app_id')
            token = get_api_key('FACEBOOK', 'access_token')
            appsecret = get_api_key('FACEBOOK', 'app_secret')

            canvas_url = 'http://localhost:8000/login_success'
            # 'https://www.facebook.com/connect/login_success.html'
            perms = ['manage_pages', 'publish_pages']

            graph = facebook.GraphAPI(access_token=token, version='2.12')

            # get url for authenticating user
            url = graph.get_auth_url(app_id, canvas_url, perms)

            webbrowser.open(url)
            FacebookApi.wait_for_request(server_class=Server, handler_class=Handler)

            global code  # pylint: disable=global-statement

            # get the code returned from authenticating user
            real_code = FacebookApi.parse_code(code)

            # send request for auth token with the code
            auth = graph.get_access_token_from_code(
                code=real_code,
                redirect_uri=canvas_url, app_id=app_id, app_secret=appsecret,
            )

            # get the actual token
            actual_token = json.dumps(auth)
            print('token = ' + actual_token)

            # update the config file
            update_api_key('FACEBOOK', 'auth_token', actual_token)
            update_api_key('FACEBOOK', 'has_token', 'true')
        except Exception:
            print('Unsuccessful attempt to get access token')
            success = False

        return success

    def post_text(self, text: str) -> bool:
        success = True
        try:
            self.graph.put_object(parent_object='me', connection_name='feed', message=text)
        except facebook.GraphAPIError:
            print('An error occured when trying to post text.')
            success = False
        return success

    def post_video(self, url: str, text: str) -> bool:
        success = True
        try:
            self.graph.put_object(
                parent_object='me',
                connection_name='feed',
                message=text,
                link=url,
            )
        except facebook.GraphAPIError:
            print('An error occured when trying to post video.')
            success = False
        return success

    def post_photo(self, url: str, text: str) -> bool:
        success = True
        try:
            self.graph.put_photo(image=open(url, 'rb'), message=text)
        except facebook.GraphAPIError:
            print('An error occured when trying to post photo.')
            success = False
        return success

    def get_user_likes(self) -> int:
        likesCount = 0
        try:
            likes = self.graph.get_connections(id='me', connection_name='likes')
            likesCount = len(list(likes))
        except facebook.GraphAPIError:
            print('An error occured when trying to get user likes.')
        return likesCount

    def get_user_followers(self, text: str) -> List[str]:
        friend_list = [text]
        try:
            friends = self.graph.get_connections(id='me', connection_name='friends')
            friend_list = list(friends)
        except facebook.GraphAPIError:
            print('An error occured when trying to get user likes.')
        return friend_list

    def remove_post(self, post_id: str) -> bool:
        success = True
        try:
            self.graph.delete_object(id=post_id)
        except facebook.GraphAPIError:
            print('An error occured when trying to post photo.')
            success = False
        return success
