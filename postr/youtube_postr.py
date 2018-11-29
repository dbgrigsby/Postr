import random
import time
import http.client
from typing import List, Any, Dict
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
        self.channel_id = channels_list_by_id(
            self.build,
            part='snippet,contentDetails,statistics',
            mine='True',
        )['items'][0]['id']

    def get_refresh_token(self) -> Any:
        # Follow the prompt to give an access code
        credentials = self.flow.run_console()
        return credentials.refresh_token

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        # No text to be posted on YouTube
        return False

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        self.upload_video(url, text, text, 22, '', 'public',)
        return True

    def upload_video(
        self,
        file: str, title: str, description: str,
        category: int, keywords: str, privacy_status: str,
    ) -> Any:
        args = {
            'file': file, 'title': title, 'description': description,
            'category': category, 'keywords': keywords, 'privacy_status': privacy_status,
        }
        try:
            initialize_upload(self.build, args)
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        # No photos on YouTube
        return False

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has total between link and client'''
        # Returns subscriber count instead
        return int(channels_list_by_id(
            self.build,
            part='statistics',
            mine='true',
        )['items'][0]['statistics']['subscriberCount'])

    def get_user_videos(self) -> str:
        ''' This method returns the video ids of this user.'''
        return str(videos_list_by_id(
            self.build,
            part='snippet,contentDetails,statistics',
            id='Ks-_Mh1QhMc',
        ))

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        # Not possible to get a list of subscriber names, as it is anonymous.
        return None  # type: ignore

    def remove_post(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the success of this action'''
        videos_delete(self.build, id=post_id)
        return True

# Remove keyword arguments that are not set


def videos_delete(client: Any, **kwargs: str) -> Any:
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().delete(
        **kwargs,
    ).execute()

    return response


def remove_empty_kwargs(**kwargs: str) -> Dict[Any, Any]:
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def channels_list_by_id(client: Any, **kwargs: str) -> Any:
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.channels().list(
        **kwargs,
    ).execute()

    return response


def videos_list_by_id(client: Any, **kwargs: str) -> Any:
    # See full sample for function
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().list(
        **kwargs,
    ).execute()

    return response


def generate_build(credentials: Credentials) -> Any:
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_key(key: str) -> Any:
    """Gets a specified key for the reddit API """
    return config.get_api_key('YouTube', key)


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


def initialize_upload(client: Any, options: dict) -> Any:
    tags = None
    if options['keywords']:
        tags = options['keywords'].split(',')

    body = dict(
        snippet=dict(
            title=options['title'],
            description=options['description'],
            tags=tags,
            categoryId=options['category'],
        ),
        status=dict(
            privacyStatus=options['privacy_status'],
        ),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = client.videos().insert(
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
        media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True),
    )

    resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.


def resumable_upload(request: Any) -> Any:
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


new_youtube = Youtube()
print(new_youtube.channel_id)
