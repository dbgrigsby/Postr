# Facebook API

from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import json
from typing import Type, List
import config
import facebook
from api_interface import ApiInterface

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

        if config.get_api_key('FACEBOOK', 'has_token') == 'true':

            authToken = config.get_api_key('FACEBOOK', 'auth_token')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version='2.12',
            )
        else:  # may need to just auth user with no has_token check
            # need to auth  user
            FacebookApi.authenticate()

            authToken = config.get_api_key('FACEBOOK', 'authToken')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version='2.12',
            )

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
    def authenticate() -> None:  # in future, add check for if the login auth fails
        # get all values needed for auth
        app_id = config.get_api_key('FACEBOOK', 'app_id')
        token = config.get_api_key('FACEBOOK', 'access_token')
        appsecret = config.get_api_key('FACEBOOK', 'app_secret')

        canvas_url = 'http://localhost:8000/login_success'
        # 'https://www.facebook.com/connect/login_success.html'
        perms = ['manage_pages', 'publish_pages']

        test = facebook.GraphAPI(access_token=token, version='2.12')

        # get url for authenticating user
        url = test.get_auth_url(app_id, canvas_url, perms)

        webbrowser.open(url)
        FacebookApi.wait_for_request(server_class=Server, handler_class=Handler)

        global code  # pylint: disable=global-statement

        # get the code returned from authenticating user
        real_code = FacebookApi.parse_code(code)

        # print('Code = ' + real_code)

        # send request for auth token with the code
        auth = test.get_access_token_from_code(
            code=real_code,
            redirect_uri=canvas_url, app_id=app_id, app_secret=appsecret,
        )

        # get the actual token
        actual_token = json.dumps(auth)
        print('token = ' + actual_token)

        # update the config file
        config.update_api_key('FACEBOOK', 'auth_token', actual_token)
        config.update_api_key('FACEBOOK', 'has_token', 'true')

    def post_text(self, text: str) -> bool:
        self.graph.put_object(parent_object='me', connection_name='feed', message=text)
        return True

    def post_video(self, url: str, text: str) -> bool:
        self.graph.put_object(
            parent_object='me',
            connection_name='feed',
            message=text,
            link=url,
        )
        return True

    def post_photo(self, url: str, text: str) -> bool:
        self.graph.put_photo(image=open(url, 'rb'), message=text)
        return True

    def get_user_likes(self) -> int:
        self.graph.get_connections(id='me', connection_name='friends')
        return 0

    # def get_user_followers(self) -> List[str]:
        # self.graph.get_connections(id='me', connection_name='friends')
        # return ['nope']

    def get_user_followers(self, text: str) -> List[str]:
        self.graph.get_connections(id='me', connection_name='friends')
        return [text]

    def remove_post(self, post_id: str) -> bool:
        self.graph.delete_object(id=post_id)
        return True


# test = FacebookApi()
