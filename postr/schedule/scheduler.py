# scheduler class basics
from datetime import datetime

from media_object import MediaObject
from platform_enum import Platform


class Scheduler():

    @staticmethod
    # pylint: disable=unused-argument
    def schedulePost(mediaObject: MediaObject, time: datetime) -> None:
        ''' This method take an enum for the type of post to be created,
        a mediaObject that contains the information to be posted, and
        the time at which to post the data '''
        print('schedule complete')

    # pylint: disable=unused-argument
    @staticmethod
    def scheduleDelete(postId: str, platform: Platform, time: datetime) -> None:
        ''' This method take the id of the post to be deleted'''
