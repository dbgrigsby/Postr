# mediaObject class
from media_type_enum import MediaType
from platform_enum import Platform


class MediaObject:
    ''' This class will have no set methods,
    but only certain data can be saved '''

    # id : the id of the media object
    id = ""

    # platform : the platform for which this media is intended - facebook
    platform = Platform.FACEBOOK

    # media-type : text, video, photo
    media_type = MediaType.TEXT

    # text: the text associated with
    text = ""

    # photourl
    photourl = ""

    # videourl
    videourl = ""
