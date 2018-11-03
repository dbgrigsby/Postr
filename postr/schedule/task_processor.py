from typing import List
from typing import Set
from typing import Any
from typing import Dict
from postr.config import get_api_key

from postr.reddit_postr import Reddit
from postr import discord_api
from postr.twitter_postr import Twitter
from postr.fbchat_api import FacebookChatApi

api_to_instance: Dict[str, Any] = {
    'discord': discord_api.discord_client,
    'reddit': Reddit(),
    'twitter': Twitter(),
    'facebook': FacebookChatApi
    (
        email=get_api_key('facebook', 'email') or '',
        password=get_api_key('facebook', 'password') or '',
    ),
}

api_to_function: Dict[str, Any] = {
    'discord': {
        'instance': '',
        'is_async': True,
        'supported_actions': {
            'post_text': {
                'function_call': api_to_instance['discord'].post_text,
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': api_to_instance['discord'].post_image,
                'arguments': {'MediaPath': 'image_filepath'},
            },
            'update_bio': {
                'function_call': api_to_instance['discord'].update_status,
                'arguments': {'OptionalText': 'status'},
            },
        },
    },
    'reddit': {
        'post_text': '',
        'post_photo': '',
        'remove_post': '',
        'update_bio': '',
    },
    'twitter': {
        'post_text': '',
        'post_photo': '',
        'remove_post': '',
        'update_bio': '',
    },
    'facebook': {
        'post_text': '',
        'post_photo': '',
        'remove_post': '',
        'update_bio': '',
    },
}


def has_required_arguments(api: str, action: str, arguments: Set[str]) -> bool:
    required_arguments: Set[str] = api_to_function[api]['supported_actions'][action]['arguments'].keys()
    return arguments == required_arguments


def get_existing_arguments(task: Dict[str, Any]) -> Set[str]:
    arguments: Set[str] = set()
    if task['Comment']:
        arguments.add(task['Comment'])

    if task['MediaPath']:
        arguments.add(task['MediaPath'])

    if task['OptionalText']:
        arguments.add(task['OptionalText'])

    return arguments


def create_command(task: Dict[str, Any]) -> str:
    task.keys()
    return ''


async def run_task(task: Dict[str, Any]) -> None:
    apis = task['Platforms'].split(',')
    for api in apis:
        if api not in api_to_function.keys():
            continue

        supported_actions = api_to_function[api]['supported_actions'].keys()
        if task['Action'] not in supported_actions:
            continue

        given_arguments = get_existing_arguments(task)
        if not has_required_arguments(api=api, action=task['Action'], arguments=given_arguments):
            continue

        command = create_command(task)

        if api_to_function[api]['is_async'] is True:
            command = f'await {command}'

        eval(command)  # pylint: disable=W0123


async def process_scheduler_events(tasks: List[Dict[str, Any]]) -> None:
    for task in tasks:
        run_task(task)
