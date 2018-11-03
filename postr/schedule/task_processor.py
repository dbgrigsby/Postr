from typing import List
from typing import Set
from typing import Any
from typing import Dict
from postr.postr_logger import make_logger

from postr.reddit_postr import Reddit
from postr import discord_api
from postr.twitter_postr import Twitter
from postr.fbchat_api import FacebookChatApi


log = make_logger('task_processor')

api_to_instance: Dict[str, Any] = {
    'discord': discord_api.discord_client,
    'reddit': Reddit(),
    'twitter': Twitter(),
    'facebook': FacebookChatApi(),
}

api_to_function: Dict[str, Any] = {
    'discord': {
        'is_async': True,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["discord"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["discord"].post_image',
                'arguments': {'MediaPath': 'image_filepath'},
            },
            'update_bio': {
                'function_call': 'api_to_instance["discord"].update_status',
                'arguments': {'OptionalText': 'status'},
            },
        },
    },
    'reddit': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["reddit"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["reddit"].post_photo',
                'arguments': {'MediaPath': 'url', 'OptionalText': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["reddit"].update_status',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'twitter': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["twitter"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["twitter"].post_image',
                'arguments': {'MediaPath': 'url', 'OptionalText': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["twitter"].update_status',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'facebook': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["facebook"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["facebook"].post_image',
                'arguments': {'MediaPath': 'image_filepath'},
            },
            'update_bio': {
                'function_call': 'api_to_instance["facebook"].update_status',
                'arguments': {'OptionalText': 'status'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["facebook"].update_status',
                'arguments': {'OptionalText': 'status'},
            },
        },
    },
}


def has_required_arguments(api: str, action: str, arguments: Set[str]) -> bool:
    required_arguments: Set[str] = api_to_function[api]['supported_actions'][action]['arguments'].keys()
    return arguments == required_arguments


def get_existing_arguments(task: Dict[str, Any]) -> Set[str]:
    arguments: Set[str] = set()
    if task['Comment']:
        arguments.add('Comment')

    if task['MediaPath']:
        arguments.add('MediaPath')

    if task['OptionalText']:
        arguments.add('OptionalText')

    return arguments


def create_command(api: str, task: Dict[str, Any], given_arguments: Set[str]) -> str:
    """ Generates a string that is a valid python command
    Example: May return api_to_instance['discord'].post_text(text="wow text here", channel='123232',)
    """
    command = ''

    action = task['Action']
    action_to_perform = api_to_function[api]['supported_actions'][action]
    callable_func = action_to_perform['function_call']

    command += callable_func
    command += '('

    functions_for_actions: Dict[str, str] = api_to_function[api]['supported_actions'][action]['arguments']

    method_args = ''
    for argument in given_arguments:
        method_args += functions_for_actions[argument]
        method_args += '='
        method_args += task[argument]
        method_args += ','

    command += method_args
    command += ')'

    return command


async def run_task(task: Dict[str, Any]) -> None:
    apis = task['Platforms'].split(',')
    for api in apis:
        if api not in api_to_function.keys():
            log.error(f'{api} is not a valid api.')
            continue

        supported_actions = api_to_function[api]['supported_actions'].keys()
        action = task['Action']
        if action not in supported_actions:
            log.error(f'{action} is not a valid action.')
            continue

        given_arguments = get_existing_arguments(task)
        if not has_required_arguments(api=api, action=task['Action'], arguments=given_arguments):
            log.error(f'Provided arguments are not sufficient for API={api}.')
            continue

        command = create_command(api, task, given_arguments)

        if api_to_function[api]['is_async'] is True:
            command = f'await {command}'

        print(f'Command to be executed: {command}')

        # Run the generated string command directly as python code
        eval(command)  # pylint: disable=W0123


async def process_scheduler_events(tasks: List[Dict[str, Any]]) -> None:
    for task in tasks:
        run_task(task)
