# api interface that all api classes must extend
import asyncio
from typing import List

import discord

from ..api_interface import ApiInterface
from ..config import get_api_key


class Discord(ApiInterface):

    def __init__(self) -> None:
        self.client = discord.Client()
        self.default_channel = get_api_key('Discord', 'default_channel')

    def post_text(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        channel_id = self.default_channel
        try:
            self.client.send_message(channel_id, text)
            return True
        except Exception as exp:
            print(f'Failed to send message: {exp}')
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

    async def set_default_channel(self, channel_id: str) -> bool:
        print('Tried to change default channel')
        try:
            await self.client.send_message(
                client.get_channel(channel_id),
                f'Default channel changed to <#{channel_id}>',
            )
            print(f'Default channel changed to {channel_id}')
            self.default_channel = channel_id
            return True
        except Exception as e:
            print(f'Failed to set default channel to channel with channel id={channel_id}')
            print(e)
            return False


discord_api = Discord()
client = discord_api.client


@client.event
async def on_ready() -> None:
    print(f'Logged in as{client.user.name}#{client.user.discriminator}')
    print(f'ID: {client.user.id}')
    await discord_api.set_default_channel('499395129992413196')


@client.event
async def on_message(message: discord.message) -> None:
    print(f'New message received in {message.channel.name} from {message.author}: {message.content}')
    print(f'Message Channel: {message.channel}')
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
        print(message.channel)

if __name__ == '__main__':
    bot_token = get_api_key('Discord', 'bot_token')
    client.run(bot_token)
    discord_api.post_text('Wow a test post!')
