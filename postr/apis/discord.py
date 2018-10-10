# api interface that all api classes must extend
import asyncio
from typing import List

import discord

from ..api_interface import ApiInterface


class Discord(ApiInterface):

    client = discord.Client()

    def __init__(self) -> None:
        self.client = discord.Client()
        self.client.run('NDIyODIyMDQ5ODI5MDkzMzc3.DYhXng.oBevkHcyRVcVa87upnxdKO7nMfg')

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        return False

    def post_video(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the video the user
        want to post and returns the success of this action'''
        return False

    def post_photo(self, url: str, text: str) -> bool:
        ''' This method takes in the url for the photo the user
        want to post and returns the success of this action'''
        return False

    def get_user_likes(self) -> int:
        ''' This method returns the number of likes a user has'''
        return -1

    def get_user_followers(self, text: str) -> List[str]:
        ''' This method returns a list of all the people that
        follow the user'''
        return None  # type: ignore

    def remove_post(self, post_id: str) -> bool:
        ''' This method removes the post with the specified id
        and returns the successs of this action'''
        return False

    @client.event
    async def on_ready(self) -> None:
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')

    @client.event
    async def on_message(self, message: discord.message) -> None:
        if message.content.startswith('!test'):
            counter = 0
            tmp = await self.client.send_message(message.channel, 'Calculating messages...')
            async for log in self.client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1

            await self.client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await self.client.send_message(message.channel, 'Done sleeping')
