# scheduler class basics
import datetime

from media_object import MediaObject
from platform_enum import Platform


class Scheduler():

    def schedulePost(mediaObject: MediaObject, time: datetime):
        ''' This method take an enum for the type of post to be created,
        a mediaObject that contains the information to be posted, and
        the time at which to post the data '''
        print("schedule complete")

    def scheduleDelete(postId: str, platform: Platform, time: datetime):
        ''' This method take the id of the post to be deleted'''
