# tumblr api test
import sys
from unittest.mock import patch
from postr import tumblr_api
sys.path.insert(0, '../postr')


client = tumblr_api.TumblrApi()


def test_post_text() -> None:
    with patch('pytumbr.TumblrRestClient.create_text') as mock_post:
        mock_post.return_value = None
        client.post_text('This is the text I want to post!')
    mock_post.assert_called()


def test_post_photo() -> None:
    with patch('pytumbr.TumblrRestClient.create_photo') as mock_post_local:
        mock_post_local.return_value = None
        client.post_photo('/some/path/', 'This is the photo I want to post!')
    mock_post_local.assert_called()

    with patch('pytumbr.TumblrRestClient.create_photo') as mock_post_remote:
        mock_post_remote.return_value = None
        client.post_photo('www.somesite.com', 'This is the photo I want to post!')
    mock_post_remote.assert_called()


def test_post_video() -> None:
    with patch('pytumbr.TumblrRestClient.create_video') as mock_post_local:
        mock_post_local.return_value = None
        client.post_video('/some/path/', 'This is the video I want to post!')
    mock_post_local.assert_called()

    with patch('pytumbr.TumblrRestClient.create_video') as mock_post_remote:
        mock_post_remote.return_value = None
        client.post_video('www.somesite.com', 'This is the video I want to post!')
    mock_post_remote.assert_called()


# def test_get_user_likes() -> None:

# def test_get_user_followers() -> None:

# def test_remove_post() -> None:
