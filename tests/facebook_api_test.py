# facebook api test
import sys
# from unittest.mock import patch
# from pathlib import Path
# import pytest
from postr import facebook_api
# from postr import config
sys.path.insert(0, '../postr')


class Object():
    name: str = ''
    uid: str = ''
    first_name: str = ''
    last_name: str = ''
    text: str = ''


client = facebook_api.FacebookApi()


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
