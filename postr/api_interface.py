# api interface that all api classes must extend
import abc


class ApiInterface(abc.ABC):

    @abc.abstractmethod
    def postText(s: str):
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        return True

    @abc.abstractmethod
    def postVideo(url, text):
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        return True

    @abc.abstractmethod
    def postPhoto(url, text):
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        return True

    @abc.abstractmethod
    def getUserLikes():
        ''' This method returns the number of likes a user has'''
        return -1

    @abc.abstractmethod
    def getUserFollowers(stringTxt):
        ''' This method returns a list of all the people that
        follow the user'''
        return None

    @abc.abstractmethod
    def removePost(postId):
        ''' This method removes the post with the specified id
        and returns the successs of this action'''
        return True
