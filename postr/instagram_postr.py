from typing import List
from .api_interface import ApiInterface


class Instagram(ApiInterface):
    def post_text(self, text: str) -> bool:
        return False

    def post_video(self, url: str, text: str) -> bool:
        return False

    def post_photo(self, url: str, text: str) -> bool:
        return False

    def get_user_likes(self) -> int:
        return -1

    def get_user_followers(self, text: str) -> List[str]:
        return [text]

    def remove_post(self, post_id: str) -> bool:
        return False
