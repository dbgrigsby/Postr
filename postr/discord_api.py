# api interface that all api classes must extend
import asyncio
# from discord.ext import commands
import discord as api
from .postr_logger import make_logger
from .config import get_api_key
from .config import update_api_key

client = api.Client()
default_channel = get_api_key('Discord', 'default_channel') or ''
log = make_logger('discord')


async def post_text_async(text: str, channel: str = default_channel) -> bool:
    ''' This method takes in the text the user want to post
    and returns the success of this action'''
    log.info(f'Trying to post "{text}" to {default_channel}')
    try:
        discord_channel = client.get_channel(channel)
        await client.send_message(discord_channel, text)
        log.info(f'Bot sent to {discord_channel.name} message: {text}')
        return True
    except Exception as exp:
        log.error(f'Failed to send message: {exp}')
        return False


async def set_default_channel(channel_id: str) -> bool:
    log.info('Tried to change default channe to channel_id')
    try:
        await post_text_async(text=f'Default channel changed to {channel_id}', channel=channel_id)
        global default_channel  # pylint: disable=W0603
        default_channel = channel_id
        update_api_key('Discord', 'default_channel', default_channel)
        log.info(f'Default channel changed to {channel_id}')
        return True
    except Exception as e:
        log.error(f'Failed to set default channel to channel with channel id={channel_id}')
        log.error(e)
        return False


async def post_announcement(text: str) -> None:
    announcements_channel = get_api_key(api='Discord', key='announcements_channel') or ''
    await post_text_async(announcements_channel, text)


@client.event
async def on_ready() -> None:
    log.info(f'Logged in as {client.user.name}#{client.user.discriminator}')
    log.info(f'ID: {client.user.id}')
    # await set_default_channel(get_api_key(api='Discord', key='default_channel') or 'None')
    await post_text_async('Wow a test post!')


@client.event
async def on_message(message: api.message) -> None:
    log.info(f'New message received in {message.channel.name} from {message.author}: {message.content}')
    if message.content.startswith('!rest'):
        await client.send_message(message.channel, 'Resting for 5 seconds')
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done resting')
    elif message.content.startswith('!default'):
        new_channel = message.channel.name
        await set_default_channel(new_channel)
        await post_text_async('Updated new channel to this one')
    elif message.content.startswith('!'):
        await client.add_reaction(message, '\N{OK HAND SIGN}')
    else:
        pass

if __name__ == '__main__':
    bot_token = get_api_key('Discord', 'bot_token')
    client.run(bot_token)
    # bot.run(bot_token)
