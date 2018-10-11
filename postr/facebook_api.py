# Facebook API
# from typing import List
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import json
from typing import Type
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
        output += '<body><h1>Thanks For Authenticationg with Postr!</h1>'
        output += '<p>You can close this tab.</p>'
        output += '</body></html>'
        self.wfile.write(output.encode())


class Server(HTTPServer):
    pass


class FacebookApi(ApiInterface):

    def __init__(self) -> None:
        # fbInfo = config._current_config()['FACEBOOK']
        if config.get_api_key('FACEBOOK', 'isLoggedIn') == 'true':
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

            app_id = config.get_api_key('FACEBOOK', 'app_id')
            canvas_url = 'https://www.facebook.com/connect/login_success.html'
            # 'https://127.0.0.1:8888'
            # "https://domain.com/that-handles-auth-response/"
            perms = ['manage_pages', 'publish_pages']
            # perms = []
            token = config.get_api_key('FACEBOOK', 'app_token')
            graphOne = facebook.GraphAPI(access_token=token, version='2.12')
            url = graphOne.get_auth_url(app_id, canvas_url, perms)
            print(url)
            # https://www.facebook.com/login
            webbrowser.open(url)
            # r = requests.get(url)
            # to set auth token, we need to ask user for permission
            # url = http://127.0.0.1:8888do i need port?
            # print('about to print the damn thing')

            # print(r.url)
            # print(r.history[0].url)
            # print(r.history[1].content)

            val = 'testing'
            # config.update_api_key('FACEBOOK', 'isLoggedIn', 'true')
            config.update_api_key('FACEBOOK', 'auth_token', val)

            # create graph for user
            authToken = config.get_api_key('FACEBOOK', 'auth_token')
            self.graph = facebook.GraphAPI(
                access_token=authToken,
                version='2.12',
            )

    @staticmethod
    def wait_for_request(
        server_class: Type[HTTPServer],  # pylint: disable=bad-continuation
        handler_class: Type[BaseHTTPRequestHandler],  # pylint: disable=bad-continuation
    ) -> None:  # pylint: disable=bad-continuation
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        httpd.timeout = 10
        try:
            httpd.handle_request()  # this can get me the code !!!!
        except KeyboardInterrupt:
            pass
        httpd.server_close()

    @staticmethod
    def parseCode(code_str: str) -> str:
        end = len(code_str)
        # get index of =
        equals_index = code_str.find('=')
        actual_code = code_str[equals_index + 1: end]
        return actual_code

    @staticmethod
    def extract_access_token(dic: dict) -> str:
        return str(dic['access_token'])

    def authenticate(self) -> None:

        app_id = config.get_api_key('FACEBOOK', 'app_id')
        canvas_url = 'http://localhost:8000/login_success'
        # 'https://www.facebook.com/connect/login_success.html'
        perms = ['manage_pages', 'publish_pages']

        token = config.get_api_key('FACEBOOK', 'access_token')
        appsecret = config.get_api_key('FACEBOOK', 'app_secret')
        test = facebook.GraphAPI(access_token=token, version='2.12')
        url = test.get_auth_url(app_id, canvas_url, perms)

        # print(url)
        webbrowser.open(url)
        self.wait_for_request(server_class=Server, handler_class=Handler)

        global code  # pylint: disable=global-statement

        real_code = self.parseCode(code)

        print('Code = ' + real_code)

        auth = test.get_access_token_from_code(
            code=real_code,
            redirect_uri=canvas_url, app_id=app_id, app_secret=appsecret,
        )

        actual = json.dumps(auth)
        print('token = ' + actual)

    # def post_text(self, s: str) -> bool:
        # self.graph.put_object(parent_object='me', connection_name='feed',
        # message=s)
        # return True

    # def post_video(self, url: str, text: str) -> bool:
        # self.graph.put_object(
        # parent_object="me",
        # connection_name="feed",
        # message=text,
        # link=url)
        # return True

    # def post_photo(self, url: str, text: str) -> bool:
        # self.graph.put_photo(image=open(url, 'rb'), message=text)
        # return True

    # def get_user_likes(self) -> int:
        # self.graph.get_connections(id='me', connection_name='friends')
        # return 0

    # def get_user_followers(self, stringTxt: str) -> List[str]:
        # self.graph.get_connections(id='me', connection_name='friends')
        # return ['nope']

    # def remov_post(self, postId: str) -> bool:
        # self.graph.delete_object(id=postId)
        # return True


# test = FacebookApi()
