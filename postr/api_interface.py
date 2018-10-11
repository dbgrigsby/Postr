# api interface that all api classes must extend
import abc
from typing import List


class ApiInterface(abc.ABC):

    @abc.abstractmethod
    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        return False

    @abc.abstractmethod
    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        return False

    @abc.abstractmethod
    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        return False

    @abc.abstractmethod
    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has'''
        return -1

    @abc.abstractmethod
    def get_user_followers(self) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        return None  # type: ignore

    @abc.abstractmethod
    def remove_post(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the successs of this action'''
        return False
