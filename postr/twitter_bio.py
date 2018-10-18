from tweepy.api import API


class TwitterBio:
    """
    Class to provide easy access for bio operations
    """

    def __init__(self, api: API) -> None:
        self.api = api

    def update_bio(self, message: str) -> None:
        """ Updates the text in your bio """
        self.api.update_profile(description=message)

    def update_name(self, new_name: str) -> None:
        """ Updates your profile name """
        self.api.update_profile(name=new_name)

    def username(self) -> str:
        """ Gets the username of the authenticated user """
        return str(self.api.me().screen_name)

    def bio(self) -> str:
        """ Gets the bio description of the authenticated user """
        return str(self.api.me().description)
