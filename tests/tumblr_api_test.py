# tumblr api test
import sys
from unittest.mock import patch
from postr import tumblr_api
sys.path.insert(0, '../postr')


client = tumblr_api.TumblrApi()


def test_post_text() -> None:
    with patch('pytumblr.TumblrRestClient.create_text') as mock_post:
        mock_post.return_value = None
        client.post_text('This is the text I want to post!')
    mock_post.assert_called()


def test_post_photo() -> None:
    with patch('pytumblr.TumblrRestClient.create_photo') as mock_post_local:
        mock_post_local.return_value = None
        client.post_photo('/some/path/', 'This is the photo I want to post!')
    mock_post_local.assert_called()

    with patch('pytumblr.TumblrRestClient.create_photo') as mock_post_remote:
        mock_post_remote.return_value = None
        client.post_photo('www.somesite.com', 'This is the photo I want to post!')
    mock_post_remote.assert_called()


def test_post_video() -> None:
    with patch('pytumblr.TumblrRestClient.create_video') as mock_post_local:
        mock_post_local.return_value = None
        client.post_video('/some/path/', 'This is the video I want to post!')
    mock_post_local.assert_called()

    with patch('pytumblr.TumblrRestClient.create_video') as mock_post_remote:
        mock_post_remote.return_value = None
        client.post_video('www.somesite.com', 'This is the video I want to post!')
    mock_post_remote.assert_called()


def test_get_user_likes() -> None:
    with patch('pytumblr.TumblrRestClient.blog_likes') as mock_get:
        like_list = []
        like_list.append('aa')
        like_list.append('bb')
        like_list.append('cc')
        like_list.append('dd')
        like_list.append('ee')

        mock_get.return_value = like_list
        like_num = client.get_user_likes()
    assert like_num == len(like_list)


def test_get_user_followers() -> None:
    with patch('pytumblr.TumblrRestClient.followers') as mock_get:
        f_list = []
        f_list.append('Sally')
        f_list.append('Dan')
        f_list.append('Tommy')
        f_list.append('Adam')
        f_list.append('Mary')
        f_list.append('Rachel')
        f_list.append('Sue')
        mock_get.return_value = f_list
        follow_list = client.get_user_followers('text')
    assert len(follow_list) == len(f_list)
    assert follow_list[1] == f_list[1]


def test_remove_post() -> None:
    with patch('pytumblr.TumblrRestClient.delete_post') as mock:
        mock.return_value = None
        client.remove_post('1122334455')
    mock.assert_called()
