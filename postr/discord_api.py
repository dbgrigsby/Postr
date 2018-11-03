from typing import Optional
from discord import Client
from discord import Channel
from discord import Game
from discord import Message
from postr import postr_logger
from postr.config import get_api_key
from postr.config import update_api_key

discord_client = Client()
log = postr_logger.make_logger('discord')


def id_to_channel(channel_id: Optional[str]) -> Channel:
    if channel_id:
        chan = discord_client.get_channel(channel_id)
        return chan
    log.error('No default channel found!')
    return next(iter(discord_client.get_all_channels()))


def default_channel_id() -> Optional[str]:
    ret = get_api_key('Discord', 'default_channel')
    return ret


async def post_text(text: str, channel_id: Optional[str] = default_channel_id()) -> bool:
    ''' This method takes in the text the user want to post
        and returns the success of this action'''
    channel = id_to_channel(channel_id)
    log.info(f'Trying to post "{text}" to {channel}')
    try:
        await discord_client.send_typing(channel)
        await discord_client.send_message(channel, text)
        log.info(f'Bot sent to {channel.name} message: {text}')
        return True
    except Exception as exp:
        log.error(f'Failed to send message: {exp}')
        return False


async def delete_bot_messages(channel_id: Optional[str] = default_channel_id()) -> bool:
    def is_me(m: Message) -> bool:
        return m.author == discord_client.user  # type: ignore
    try:
        channel = id_to_channel(channel_id)
        deleted = await discord_client.purge_from(channel, limit=100, check=is_me)
        await discord_client.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))
        return True
    except Exception as exp:
        log.error(f'Failed to delete bot messages: {exp}')
        return False


async def post_image(image_filepath: str, channel_id: Optional[str] = default_channel_id()) -> bool:
    channel = discord_client.get_channel(channel_id)
    try:
        with open(image_filepath, 'rb') as f:
            await discord_client.send_file(channel, f)
            return True
    except Exception as exp:
        log.error(f'Failed to post image: {exp}')
        return False


async def update_status(status: str) -> bool:
    try:
        game_from_status = Game(name=status)
        await discord_client.change_presence(game=game_from_status)
        return True
    except Exception as exp:
        log.error(f'Failed to update status: {exp}')
        return False


async def set_default_channel(channel_id: Optional[str] = default_channel_id()) -> bool:
    channel = id_to_channel(channel_id)
    log.info('Tried to change default channe to channel_id')
    try:
        await post_text(text=f'Default channel changed to {channel.name}', channel_id=channel_id)
        update_api_key('Discord', 'default_channel', channel.id)
        log.info(f'Default channel changed to {channel.name}')
        return True
    except Exception as e:
        log.error(f'Failed to set default channel to channel with channel id={channel.name}')
        log.error(e)
        return False


async def post_announcement(text: str) -> None:
    announcements_channel = get_api_key(api='Discord', key='announcements_channel') or ''
    await post_text(announcements_channel, text)


@discord_client.event
async def on_ready() -> None:
    log.info(f'Logged in as {discord_client.user.name}#{discord_client.user.discriminator}')
    log.info(f'ID: {discord_client.user.id}')
    await post_text('Bot started!')


@discord_client.event
async def on_message(message: Message) -> None:
    log.info(f'New message received in {message.channel.name} from {message.author}: {message.content}')
    if message.content.startswith('!default'):
        new_channel_id = message.channel.id
        await set_default_channel(channel_id=new_channel_id)
        await post_text('Updated new channel to this one')
    elif message.content.startswith('!playing'):
        await update_status(message.split('!playing')[1])
    elif message.content.startswith('!purge'):
        await delete_bot_messages(message.channel.id)
    elif message.content.startswith('!'):
        await discord_client.add_reaction(message, '\N{OK HAND SIGN}')
    else:
        pass

if __name__ == '__main__':
    bot_token = get_api_key('Discord', 'bot_token')
    discord_client.run(bot_token)
    # bot.run(bot_token)
