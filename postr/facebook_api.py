# Facebook API
from typing import List

import config
from api_interface import ApiInterface
# import facebook


class FacebookApi(ApiInterface):
    # isLoggedIn = False
    # authToken = ""
    # graph = None
    # by the time we finsh this initialization,
    # we will know that the user is logged in

    # def __init__(self):
        # if(not isLoggedIn):
            # get auth token and save it
            # authToken = "not"
            # isLoggedIn = True
        # else:
            # save auth token
            # authToken = "test"

        # graph = facebook.GraphAPI(access_token=authToken, version="2.12")

    def postText(s: str) -> bool:

        return True

    def postVideo(url: str, text: str) -> bool:
        return True

    def postPhoto(url: str, text: str) -> bool:
        return True

    def getUserLikes() -> int:
        return 0

    def getUserFollowers(stringTxt: str) -> List[str]:
        # graph.get_connections(id='me', connection_name='friends')
        return None

    def removePost(postId: str) -> bool:
        return True


print(config._git_root_dir())
print(config._current_config().sections())
