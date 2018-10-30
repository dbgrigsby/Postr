# facebook api test
import sys
from unittest.mock import patch
from postr import facebook_api
sys.path.insert(0, '../postr')


class Object():
    name: str = ''
    uid: str = ''
    first_name: str = ''
    last_name: str = ''
    text: str = ''


def get_mock_client() -> facebook_api.FacebookApi:
    with patch('postr.facebook_api.FacebookApi.authenticate') as mock_auth:
        mock_auth.return_value = False
        return facebook_api.FacebookApi()


client = get_mock_client()


def test_parse_code() -> None:
    unparsed = 'code=123456'
    code = client.parse_code(unparsed)
    assert code == '123456'

# def test_extract_access_token() -> None:

# def test_post_text() -> None:
    # with patch


# def test_get_user_likes() -> None:

# def test_get_user_followers() -> None:

# def test_() -> None:
# def test_() -> None:
# def test_() -> None:
