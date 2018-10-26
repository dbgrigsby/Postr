# test fbchat api
import sys
from unittest.mock import patch
# from postr import config
# import fbchat_api
from postr import fbchat_api
sys.path.insert(0, '../postr')


class Object():
    name: str = ''
    uid: str = ''
    first_name: str = ''
    last_name: str = ''
    text: str = ''


client = fbchat_api.FacebookChatApi('ddo3@case.edu', 'seniorproject')


def test_nothing(fbchat_test: int) -> None:
    assert fbchat_test == 17


def test_get_user_id() -> None:
    with patch('fbchat.Client.fetchAllUsers') as mock_fetch:
        user_list = []
        user1 = Object()
        user1.name = 'sally'
        user1.uid = '111222333'

        user2 = Object()
        user2.name = 'martha'
        user2.uid = '1111111'
        user_list.append(user1)
        user_list.append(user2)

        mock_fetch.return_value = user_list

        user_id1 = client.get_user_id('sally')
        user_id2 = client.get_user_id('martha')

    assert user_id1 == user1.uid
    assert user_id2 == user2.uid


def test_get_user_name() -> None:
    with patch('fbchat.Client.fetchUserInfo') as mock_fetch:
        test_dict = {}
        user1 = Object()
        user1.first_name = 'Sally'
        user1.last_name = 'Glass'

        uid = '111222333'
        test_dict[uid] = user1

        mock_fetch.return_value = test_dict

        user_name = client.get_user_name(uid)

    assert user_name == user1.first_name + ' ' + user1.last_name


def test_get_thread_name() -> None:
    with patch('fbchat.Client.fetchThreadInfo') as mock_fetch:
        test_dict = {}
        obj1 = Object()
        obj1.name = 'Game Design Chat'

        tid = '246832'
        test_dict[tid] = obj1

        mock_fetch.return_value = test_dict

        name = client.get_thread_name(tid)

    assert name == obj1.name


def test_get_messages_from_thread() -> None:
    with patch('fbchat.Client.fetchThreadMessages') as mock_fetch:
        test_list = []

        obj1 = Object()
        obj1.text = 'This is a message to you'
        test_list.append(obj1)

        obj2 = Object()
        obj2.text = 'This is a another message to you'
        test_list.append(obj2)

        obj3 = Object()
        obj3.text = 'Why are you ignoring me?'
        test_list.append(obj3)

        obj4 = Object()
        obj4.text = 'pls respond'
        test_list.append(obj4)

        mock_fetch.return_value = test_list

        actual_list = client.get_messages_from_thread('112233', 4)

    assert len(actual_list) == 4
    assert actual_list[3] == 'This is a message to you'
    assert actual_list[0] == 'pls respond'


def test_get_all_threads() -> None:
    with patch('fbchat.Client.fetchThreadList') as mock_fetch:
        test_list = []

        obj1 = Object()
        obj1.name = 'Billy'
        obj1.uid = '11111'
        test_list.append(obj1)

        obj2 = Object()
        obj2.name = 'Daniel'
        obj2.uid = '22222'
        test_list.append(obj2)

        obj3 = Object()
        obj3.name = 'Sally'
        obj3.uid = '33333'
        test_list.append(obj3)

        obj4 = Object()
        obj4.name = 'Fred'
        obj4.uid = '44444'
        test_list.append(obj4)

        mock_fetch.return_value = test_list

        actual_client = client.get_client()

        thread_dict = fbchat_api.FacebookChatApi.get_all_threads(actual_client)

    assert thread_dict['Sally'] == '33333'
    assert thread_dict['Billy'] == '11111'
    assert thread_dict['Daniel'] == '22222'
    assert thread_dict['Fred'] == '44444'


def test_get_all_users_in_chat_with() -> None:
    with patch('fbchat.Client.fetchAllUsers') as mock_fetch:
        test_list = []

        obj1 = Object()
        obj1.name = 'Billy'
        obj1.uid = '11111'
        test_list.append(obj1)

        obj2 = Object()
        obj2.name = 'Daniel'
        obj2.uid = '22222'
        test_list.append(obj2)

        obj3 = Object()
        obj3.name = 'Sally'
        obj3.uid = '33333'
        test_list.append(obj3)

        obj4 = Object()
        obj4.name = 'Fred'
        obj4.uid = '44444'
        test_list.append(obj4)

        mock_fetch.return_value = test_list

        actual_client = client.get_client()

        user_dict = fbchat_api.FacebookChatApi.get_all_users_in_chat_with(actual_client)

    assert user_dict['Sally'] == '33333'
    assert user_dict['Billy'] == '11111'
    assert user_dict['Daniel'] == '22222'
    assert user_dict['Fred'] == '44444'


def test_get_thread_id() -> None:
    with patch('fbchat.Client.searchForThreads') as mock_get:
        test_list = []

        obj1 = Object()
        obj1.name = 'Billy'
        obj1.uid = '11111'
        test_list.append(obj1)

        mock_get.return_value = test_list

        thread_id = client.get_thread_id('Billy')

    assert thread_id == obj1.uid


def test_send_local_image_with_message() -> None:
    with patch('fbchat.Client.sendLocalImage') as mock_send:
        mock_send.return_value = None

        client.send_local_image_with_message('thread_id', 'file_path', 'message')

    mock_send.assert_called()


def test_send_remote_image_with_message() -> None:
    with patch('fbchat.Client.sendRemoteImage') as mock_send:
        mock_send.return_value = None

        client.send_remote_image_with_message('thread_id', 'file_path', 'message')

    mock_send.assert_called()


def test_send_text_message() -> None:
    with patch('fbchat.Client.send') as mock_send:
        mock_send.return_value = None

        client.send_text_message('thread_id', 'message')

    mock_send.assert_called()


def test_send_local_file_with_message() -> None:
    with patch('fbchat.Client.sendLocalFiles') as mock_send:
        mock_send.return_value = None

        client.send_local_file_with_message('thread_id', 'file_path', 'message')

    mock_send.assert_called()

# TODO these methods require mcoking two objects, which I have not figured out yet
# def test_get_threads_with_unread_messages() -> None:
# def test_get_all_users_in_this_chat() -> None:
# def test_start_thread_with_users() -> None:
# def test_start_thread_with_user() -> None:
# def test_delete_thread() -> None:
