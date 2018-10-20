import discord as api
from .postr_logger import make_logger
from .config import get_api_key
from .config import update_api_key

client = api.Client()
default_channel = get_api_key('Discord', 'default_channel') or ''
log = make_logger('discord')


async def post_text(text: str, channel_id: str = default_channel) -> bool:
    ''' This method takes in the text the user want to post
    and returns the success of this action'''
    log.info(f'Trying to post "{text}" to {default_channel}')
    try:
        discord_channel = client.get_channel(channel_id)
        await client.send_typing(discord_channel)
        await client.send_message(discord_channel, text)
        log.info(f'Bot sent to {discord_channel.name} message: {text}')
        return True
    except Exception as exp:
        log.error(f'Failed to send message: {exp}')
        return False


async def delete_bot_messages(channel_id: str) -> bool:
    def is_me(m: api.message) -> bool:
        return m.author == client.user  # type: ignore
    try:
        discord_channel = client.get_channel(channel_id)
        deleted = await client.purge_from(discord_channel, limit=100, check=is_me)
        await client.send_message(discord_channel, 'Deleted {} message(s)'.format(len(deleted)))
        return True
    except Exception as exp:
        log.error(f'Failed to delete bot messages: {exp}')
        return False


async def post_image(image_filepath: str, channel_id: str) -> bool:
    channel = client.get_channel(channel_id)
    try:
        with open(image_filepath, 'rb') as f:
            await client.send_file(channel, f)
            return True
    except Exception as exp:
        log.error(f'Failed to post image: {exp}')
        return False


async def update_status(status: str) -> bool:
    try:
        game_from_status = api.Game(name=status)
        await client.change_presence(game=game_from_status)
        return True
    except Exception as exp:
        log.error(f'Failed to update status: {exp}')
        return False


async def set_default_channel(channel_id: str) -> bool:
    log.info('Tried to change default channe to channel_id')
    try:
        await post_text(text=f'Default channel changed to {channel_id}', channel_id=channel_id)
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
    await post_text(announcements_channel, text)


@client.event
async def on_ready() -> None:
    log.info(f'Logged in as {client.user.name}#{client.user.discriminator}')
    log.info(f'ID: {client.user.id}')
    await post_text('Bot started!')


@client.event
async def on_message(message: api.message) -> None:
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
        await client.add_reaction(message, '\N{OK HAND SIGN}')
    else:
        pass

if __name__ == '__main__':
    bot_token = get_api_key('Discord', 'bot_token')
    client.run(bot_token)
    # bot.run(bot_token)
