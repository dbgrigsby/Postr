# api interface that all api classes must extend
import asyncio
from typing import List
# from discord.ext import commands
import discord

from ..api_interface import ApiInterface
from ..config import get_api_key


class Discord(ApiInterface):

    def __init__(self) -> None:
        self.client = discord.Client()
        self.default_channel = get_api_key('Discord', 'default_channel')

    def post_text(self, text: str) -> bool:
        '''This method cannot be used as discord actions are asynchronous'''
        return False

    async def post_text_async(self, text: str) -> bool:
        ''' This method takes in the text the user want to post
        and returns the success of this action'''
        channel_id = self.default_channel
        try:
            await self.client.send_message(self.client.get_channel(channel_id), text)
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
# bot = commands.Bot(command_prefix='!', description="Command Parser")


@client.event
async def on_ready() -> None:
    print(f'Logged in as{client.user.name}#{client.user.discriminator}')
    print(f'ID: {client.user.id}')
    # await discord_api.set_default_channel('499395129992413196')
    await discord_api.post_text_async('Wow a test post!')


@client.event
async def on_message(message: discord.message) -> None:
    print(f'New message received in {message.channel.name} from {message.author}: {message.content}')
    if message.content.startswith('!channel'):
        messages_in_channel = 0
        tmp = await client.send_message(message.channel, 'Counting messages in channel...')
        async for msg in client.logs_from(message.channel, limit=1000):
            if msg:
                messages_in_channel += 1
        await client.edit_message(tmp, f'In total, {messages_in_channel} messages in this channel')
    elif message.content.startswith('!rest'):
        await client.send_message(message.channel, 'Resting for 5 seconds')
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done resting')
    else:
        await client.add_reaction(message, '👍')
    # else:
    #     await bot.process_commands(message)

if __name__ == '__main__':
    bot_token = get_api_key('Discord', 'bot_token')
    client.run(bot_token)
    # bot.run(bot_token)
