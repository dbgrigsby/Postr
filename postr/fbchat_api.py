# Facebook Chat API
# https://fbchat.readthedocs.io/en/master/examples.html#basic-example
from typing import List
from fbchat import Client
from fbchat.models import Message, ThreadType, FBchatException


class FacebookChatApi():

    def __init__(self, email: str, password: str) -> None:
        self.client: Client = None
        self.user_id: str = '00000'
        self.threads: dict = {}
        self.users: dict = {}

        try:
            client = Client(email, password)
            self.client = client

            # stores the user id
            self.user_id = client.uid

            # stores the name-thread_id pair for all threads this user has
            self.threads = FacebookChatApi.get_all_threads(client)

            # stores all users the logged in user is in a chat with
            self.users = FacebookChatApi.get_all_users_in_chat_with(client)

        except FBchatException:
            print('Login Failure : Cannot execute this command.')

    def get_client(self) -> Client:
        return self.client

    def get_user_id(self, name: str) -> str:
        """ Returns the userid of input person, if that person is in a chat with or
        friends with the person who logged in """
        users = self.client.fetchAllUsers()
        for user in users:
            if user.name == name:
                return str(user.uid)
        return ''

    def get_user_name(self, user_id: str) -> str:
        """ Returns the name of the user specified by the input user id """
        user_dict = self.client.fetchUserInfo(user_id)

        if not user_dict:
            name = ''
        else:
            user = user_dict[user_id]
            name = str(user.first_name + ' ' + user.last_name)

        return name

    def get_thread_name(self, thread_id: str) -> str:
        """ Returns the name of the thread specified by the input thread id """
        thread_dict = self.client.fetchThreadInfo(thread_id)

        name = ''
        if thread_dict:
            thread = thread_dict[thread_id]
            name = str(thread.name)

        return name

    def get_messages_from_thread(self, thread_id: str, number_of_messages: int) -> List[str]:
        """ Returns a list of the messages associated with the input thread id """
        messages = self.client.fetchThreadMessages(thread_id=thread_id, limit=number_of_messages)
        # Since the message come in reversed order, reverse them
        messages.reverse()

        messageList = []
        # Prints the content of all the messages
        for message in messages:
            messageList.append(message.text)
        return messageList

    @staticmethod
    def get_all_threads(client: Client) -> dict:
        """ Returns a dictionary that maps the names of all threads associated with
        the imput client with their thread ids """
        threads = client.fetchThreadList()
        thread_dict = {}
        for thread in threads:
            thread_dict[thread.name] = str(thread.uid)
        return thread_dict

    @staticmethod
    def get_all_users_in_chat_with(client: Client) -> dict:
        """ Returns a dictionary of user name and id pairs for all people the
        current user is in chats with """
        users = client.fetchAllUsers()
        user_dict = {}

        for user in users:
            user_dict[user.name] = str(user.uid)
        return user_dict

    def get_all_users_in_this_chat(self, thread_name: str) -> dict:
        """ Returns a dictionary of user name and id pairs for all people in the specified thread"""
        group = self.client.searchForGroups(self, thread_name)

        participants_ids = group[0].participants

        people_in_this_chat = {}
        if participants_ids is not None:
            for key in self.users:
                if self.users[key] in participants_ids:
                    people_in_this_chat[key] = self.users[key]

        return people_in_this_chat

    def start_thread_with_users(self, message: str, user_ids: List) -> None:
        """ Create a new thread with the specified users and initial meessage """
        self.client.createGroup(message, user_ids)

        self.threads = FacebookChatApi.get_all_threads(self.client)
        self.users = FacebookChatApi.get_all_users_in_chat_with(self.client)

    def start_thread_with_user(self, message: str, user_id: str) -> None:
        """ Create a new thread with the specified user and initial meessage  """
        user_ids = [user_id]
        self.start_thread_with_users(message, user_ids)

    def delete_thread(self, thread_id: str) -> None:
        """ Delete specified thread from users threads """
        self.client.deleteThreads(thread_id)
        # update the user threads and users dicts
        self.threads = FacebookChatApi.get_all_threads(self.client)
        self.users = FacebookChatApi.get_all_users_in_chat_with(self.client)

    def get_thread_id(self, thread_name: str) -> str:
        """ Returns the thread id  associated with the input thread name """
        thread = self.client.searchForThreads(thread_name)[0]
        return str(thread.uid)

    def send_local_image_with_message(self, thread_id: str, image_path: str, message: str) -> None:
        """ Sends an image with a message to specified thread """
        self.client.sendLocalImage(
            image_path, message=Message(text=message),
            thread_id=thread_id, thread_type=ThreadType.GROUP,
        )

    def send_local_image_no_message(self, thread_id: str, image_path: str) -> None:
        """ Sends an image with no message to specified thread """
        self.client.sendLocalImage(image_path, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

    def send_remote_image_with_message(self, thread_id: str, image_url: str, message: str) -> None:
        """ Sends an image with a message to specified thread """
        self.client.sendRemoteImage(
            image_url, message=Message(text=message),
            thread_id=thread_id, thread_type=ThreadType.GROUP,
        )

    def send_remote_image_no_message(self, thread_id: str, image_url: str) -> None:
        """ Sends an image with no message to specified thread """
        self.client.sendRemoteImage(image_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

    def send_text_message(self, thread_id: str, message: str) -> None:
        """ Sends a message to specified thread """
        self.client.send(Message(text=message), thread_id, thread_type=ThreadType.GROUP)

    def send_local_file_with_message(self, thread_id: str, file_path: str, message: str) -> None:
        """ Sends an file with a message to specified thread """
        self.client.sendLocalFiles(
            file_path, message=Message(text=message),
            thread_id=thread_id, thread_type=ThreadType.GROUP,
        )

    def send_local_file_no_message(self, thread_id: str, file_path: str) -> None:
        """ Sends an image with no message to specified thread """
        self.client.sendLocalFiles(file_path, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

    def block_user(self, user_id: str) -> None:
        """ Block a specific user """
        self.client.blockUser(user_id)

    def unblock_user(self, user_id: str) -> None:
        """ Unblock a specific user """
        self.client.unblockUser(user_id)

    def remove_friend(self, user_id: str) -> None:
        """ Unfriend the input user """
        self.client.removeFriend(friend_id=user_id)

    def remove_user_from_thread(self, user_id: str, thread_id: str) -> None:
        """ Remove specific user from thread"""
        self.client.removeUserFromGroup(user_id=user_id, thread_id=thread_id)

    def change_name_of_thread(self, thread_id: str, name: str) -> None:
        """ Change the name of the specified thread """
        self.client.changeThreadTitle(name, thread_id=thread_id, thread_type=ThreadType.GROUP)

    def change_user_name_in_thread(self, user_name: str, thread_id: str, name: str) -> None:
        """ Change the name of the spcified user in the thread """
        user_id = self.users[user_name]
        self.client.changeNickname(name, user_id, thread_id=thread_id, thread_type=ThreadType.GROUP)

    def get_threads_with_unread_messages(self) -> dict:
        """ Return a dictionary that maps thread_ids with thread names for threads with unread messages
        key = thread name"""

        unread_thread_ids = self.client.fetchUnread()
        thread_dict = {}
        if unread_thread_ids is not None:
            for key in self.threads:
                if self.threads[key] in unread_thread_ids:
                    thread_dict[key] = self.threads[key]

        return thread_dict

    def get_threads_with_unseen_messages(self) -> dict:
        """ Return a dictionary that maps thread_ids with thread names for threads with unseen messages
        key : thread name """
        unseen_thread_ids = self.client.fetchUnseen()
        thread_dict = {}
        if unseen_thread_ids is not None:
            for key in self.threads:
                if self.threads[key] in unseen_thread_ids:
                    thread_dict[key] = self.threads[key]

        return thread_dict

    def wave_in_message(self, thread_id: str) -> None:
        """ Sends a 'wave' to the specified thread """
        self.client.wave(wave_first=True, thread_id=thread_id, thread_type=ThreadType.GROUP)
