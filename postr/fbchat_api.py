# Facebook Chat API
# https://fbchat.readthedocs.io/en/master/examples.html#basic-example
from typing import List
from fbchat import Client
# from fbchat.models import *


class FacebookChatApi():

    def __init__(self, email: str, password: str) -> None:
        client = Client(email, password)
        self.client = client
        self.user_id = client.uid
        # todo - add all threads as a name-thread id pair
        self.threads = FacebookChatApi.get_all_threads(client)

    def get_user_id(self, name: str) -> str:
        users = self.client.fetchAllUsers()
        for user in users:
            if user.name == name:
                return str(user.uid)
        return ''

    def get_messages_from_thread(self, thread_id: str, number_of_messages: int) -> List[str]:
        messages = self.client.fetchThreadMessages(thread_id=thread_id, limit=number_of_messages)
        # Since the message come in reversed order, reverse them
        messages.reverse()

        messageList = []
        # Prints the content of all the messages
        for message in messages:
            messageList.append(message.text)
            # print(message.text)
        return messageList

    @staticmethod
    def get_all_threads(client: Client) -> dict:
        threads = client.fetchThreadList()
        thread_dict = {}
        for thread in threads:
            thread_dict[thread.name] = str(thread.uid)
        return thread_dict

    def print_all_threads(self) -> None:
        threads = self.client.fetchThreadList()
        print(threads[0].uid)
        print('Threads: {}'.format(threads))

    def get_thread_id(self, thread_name: str) -> str:
        thread = self.client.searchForThreads(thread_name)[0]
        return str(thread.uid)

    # def get_all_users_in_chat_with(self) -> dict:
        # dict has name to id mapping
        # return {"test":"test"}

    # def send_local_image(self, thread_id: str,image_path: str) -> None:
        # todo
        # return

    # def send_remote_image(self, thread_id: str, image_url: str) -> None:
        # todo
        # return

    # def send_text_message(self, thread_id: str, ) -> None:
        # todo
        # return
    # def change_nickname_for_thread(self, thread_id: str, nick_name:str) -> None:
        # self.client.changeThreadTitle(str, thread_id=thread_id, thread_type=ThreadType.GROUP)
