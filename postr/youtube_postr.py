import random
import time
import argparse
import http.client
from typing import List, Any
import httplib2

from postr.api_interface import ApiInterface
from postr import config
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class Youtube(ApiInterface):

    def __init__(self) -> None:
        self.flow = InstalledAppFlow.from_client_config(
            {'installed':
             {
                 'client_id': get_key('client_id'),
                 'project_id': get_key('project_id'),
                 'auth_uri': get_key('auth_uri'),
                 'token_uri': get_key('token_uri'),
                 'auth_provider_x509_cert_url':
                 get_key('auth_provider_x509_cert_url'),
                     'client_secret': get_key('client_secret'),
             }},
            SCOPES,
            redirect_uri=get_key('redirect_uri'),
        )
        self.credentials = Credentials(
            None,
            refresh_token=get_key('refresh_token'),
            token_uri='https://accounts.google.com/o/oauth2/token',
            client_id=get_key('client_id'),
            client_secret=get_key('client_secret'),
        )
        self.build = generate_build(self.credentials)

    def get_refresh_token(self) -> Any:
        # Follow the prompt to give an access code
        credentials = self.flow.run_console()
        return credentials.refresh_token

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        return True

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        return True

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        return True

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has total between link and client'''
        return 0

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
        and returns the success of this action'''
        # TODO failure checking
        return True


# TODO type ignore fix
def generate_build(credentials) -> Any:  # type: ignore
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_key(key: str) -> Any:
    """Gets a specified key for the reddit API """
    return config.get_api_key('YouTube', key)


def channels_list_by_username(service, **kwargs):  # type: ignore
    results = service.channels().list(
        **kwargs,
    ).execute()

    print('This channel\'s ID is %s. Its title is %s, and it has %s views.' %
          (
              results['items'][0]['id'],
              results['items'][0]['snippet']['title'],
              results['items'][0]['statistics']['viewCount'],
          ))


new_Youtube = Youtube()


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error, IOError, http.client.NotConnected,
    http.client.IncompleteRead, http.client.ImproperConnectionState,
    http.client.CannotSendRequest, http.client.CannotSendHeader,
    http.client.ResponseNotReady, http.client.BadStatusLine,
)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')


# TODO type ignore fix
def initialize_upload(youtube, options) -> Any:  # type: ignore
    tags = None
    if options.keywords:
        tags = options.keywords.split(',')

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category,
        ),
        status=dict(
            privacyStatus=options.privacyStatus,
        ),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(list(body.keys())),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting 'chunksize' equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True),
    )

    resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.


# TODO type ignore fix
def resumable_upload(request) -> Any:  # type: ignore
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            _, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print('Video id "%s" was successfully uploaded.' % response['id'])
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (
                    e.resp.status,
                    e.content,
                )
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)


# TODO type ignore fix
def uploadvideo(file, title, description, category, keywords, privacy_status) -> Any:  # type: ignore
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=False, help='Video file to upload', default=file)
    parser.add_argument('--title', help='Video title', default=title)
    parser.add_argument('--description', help='Video description', default=description)
    parser.add_argument(
        '--category', default=category,
        help='Numeric video category. ' + 'See https://developers.google.com/youtube/v3/docs/videoCategories/list',
    )
    parser.add_argument(
        '--keywords', help='Video keywords, comma separated',
        default=keywords,
    )
    parser.add_argument(
        '--privacyStatus', choices=VALID_PRIVACY_STATUSES,
        default=privacy_status, help='Video privacy status.',
    )
    args = parser.parse_args()

    try:
        initialize_upload(new_Youtube.build, args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


uploadvideo(
    'C:\\Users\\Tommy\\Pictures\\dank\\To be continued greenscreen.mp4',
    'test upload', 'this is a test', 22, 'arg', 'private',
)
