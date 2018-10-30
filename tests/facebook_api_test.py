# facebook api test
import sys
from unittest.mock import patch
from postr import facebook_api
sys.path.insert(0, '../postr')


def get_mock_client() -> facebook_api.FacebookApi:
    with patch('postr.facebook_api.FacebookApi.authenticate') as mock_auth:
        mock_auth.return_value = False
        return facebook_api.FacebookApi()


client = get_mock_client()


def test_parse_code() -> None:
    unparsed = 'code=123456'
    code = client.parse_code(unparsed)
    assert code == '123456'


def test_extract_access_token() -> None:
    test_dict = {}
    test_dict['access_token'] = '1122334455'
    access_token = client.extract_access_token(test_dict)

    assert access_token == test_dict['access_token']


def test_post_text() -> None:
    with patch('facebook.GraphAPI.put_object') as mock_put:
        mock_put.return_value = None
        client.post_text('This is the text I want to post!')
    mock_put.assert_called()


def test_post_video() -> None:
    with patch('facebook.GraphAPI.put_object') as mock_put:
        mock_put.return_value = None
        client.post_video('some_path', 'This is the video I want to post!')
    mock_put.assert_called()


def test_post_photo() -> None:
    with patch('facebook.GraphAPI.put_photo') as mock_put2:
        with patch('builtins.open') as mock_image:
            mock_put2.return_value = None
            mock_image.return_value = None
            client.post_photo('some_path', 'This is the photi I want to post!')
    mock_put2.assert_called()


def test_get_user_likes() -> None:
    with patch('facebook.GraphAPI.get_connections') as mock_get:
        like_list = []
        like_list.append('Sally')
        like_list.append('Sam')
        like_list.append('Billy')
        like_list.append('Dan')
        like_list.append('Mitch')

        mock_get.return_value = like_list
        like_count = client.get_user_likes()

    assert like_count == len(like_list)


def test_get_user_followers() -> None:
    with patch('facebook.GraphAPI.get_connections') as mock_get:
        f_list = []
        f_list.append('Sally')
        f_list.append('Sam')
        f_list.append('Billy')
        f_list.append('Dan')
        f_list.append('Mitch')

        mock_get.return_value = f_list
        friends = client.get_user_followers('text')

    assert len(friends) == len(f_list)
    mock_get.assert_called()


def test_remove_post() -> None:
    with patch('facebook.GraphAPI.delete_object') as mock_delete:
        mock_delete.return_value = None

        client.remove_post('id of post to delete')
    mock_delete.assert_called()
