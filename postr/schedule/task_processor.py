# import asyncio
from typing import List
from typing import Set
from typing import Any
from typing import Dict
from postr.postr_logger import make_logger

from postr.reddit_postr import Reddit
# from postr import discord_api
from postr.twitter_postr import Twitter
# from postr.fbchat_api import FacebookChatApi
from postr.slack_api import SlackApi
# from postr.Tumblr_api import TumblrApi
from postr.instagram_postr import Instagram
from postr.youtube_postr import Youtube
from postr.config import missing_configs_for


log = make_logger('task_processor')

api_to_instance: Dict[str, Any] = {
    # 'Discord': Discord_api if missing_configs_for('Discord') == [] else None,
    'Reddit': Reddit() if missing_configs_for('Reddit') == [] else None,
    'Twitter': Twitter() if missing_configs_for('Twitter') == [] else None,
    # 'Facebook': FacebookChatApi() if missing_configs_for('Facebook') == [] else None,
    'Slack': SlackApi() if missing_configs_for('Slack') == [] else None,
    # 'Tumblr': TumblrApi() if missing_configs_for('Tumblr') == [] else None,
    'Instagram': Instagram() if missing_configs_for('Instagram') == [] else None,
    'YouTube': Youtube() if missing_configs_for('YouTube') == [] else None,
}
# if missing_configs_for('Discord') != []:
#   api_to_instance['Discord'].main()

api_to_function: Dict[str, Any] = {
    'Discord': {
        'is_async': True,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Discord"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Discord"].post_image',
                'arguments': {'MediaPath': 'image_filepath'},
            },
            'update_bio': {
                'function_call': 'api_to_instance["Discord"].update_status',
                'arguments': {'OptionalText': 'status'},
            },
        },
    },
    'Reddit': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Reddit"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Reddit"].post_photo',
                'arguments': {'MediaPath': 'url', 'OptionalText': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Reddit"].update_status',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'Twitter': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Twitter"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Twitter"].post_image',
                'arguments': {'MediaPath': 'url', 'OptionalText': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Twitter"].update_status',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'Facebook': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Facebook"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Facebook"].post_image',
                'arguments': {'MediaPath': 'image_filepath'},
            },
            'update_bio': {
                'function_call': 'api_to_instance["Facebook"].update_status',
                'arguments': {'OptionalText': 'status'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Facebook"].delete_thread',
                'arguments': {'OptionalText': 'thread_id'},
            },
        },
    },
    'Slack': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Slack"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Slack"].post_photo',
                'arguments': {'MediaPath': 'url', 'Comment': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Slack"].remove_post',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'Tumblr': {
        'is_async': False,
        'supported_actions': {
            'post_text': {
                'function_call': 'api_to_instance["Tumblr"].post_text',
                'arguments': {'Comment': 'text'},
            },
            'post_video': {
                'function_call': 'api_to_instance["Tumblr"].post_video',
                'arguments': {'MediaPath': 'url', 'Comment': 'text'},
            },
            'post_photo': {
                'function_call': 'api_to_instance["Tumblr"].post_photo',
                'arguments': {'MediaPath': 'url', 'Comment': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Tumblr"].remove_post',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'Instagram': {
        'is_async': False,
        'supported_actions': {
            'post_photo': {
                'function_call': 'api_to_instance["Instagram"].post_photo',
                'arguments': {'MediaPath': 'url', 'Comment': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["Instagram"].remove_post',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },
    'YouTube': {
        'is_async': False,
        'supported_actions': {
            'post_video': {
                'function_call': 'api_to_instance["YouTube"].post_video',
                'arguments': {'MediaPath': 'file', 'OptionalText': 'text'},
            },
            'remove_post': {
                'function_call': 'api_to_instance["YouTube"].remove_post',
                'arguments': {'OptionalText': 'post_id'},
            },
        },
    },

}


def has_required_arguments(api: str, action: str, arguments: Set[str]) -> bool:
    required_arguments: Set[str] = api_to_function[api]['supported_actions'][action]['arguments'].keys()
    print(f'required arguments were: {required_arguments}')
    print(f'and provided arguments were {arguments}')
    return required_arguments <= arguments


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
    Example: May return api_to_instance['Discord'].post_text(text="wow text here", channel='123232',)
    """
    command = ''

    action = task['Action']
    action_to_perform = api_to_function[api]['supported_actions'][action]
    callable_func = action_to_perform['function_call']

    command += callable_func
    command += '('

    functions_for_actions: Dict[str, str] = api_to_function[api]['supported_actions'][action]['arguments']
    log.info(f'Functions for actions were... {functions_for_actions}')
    log.info(f'Given arguments were: {given_arguments}')

    method_args = ''
    for argument in given_arguments:
        if argument not in functions_for_actions:
            continue  # Scheduler provided extra argument, skip
        method_args += functions_for_actions[argument]
        method_args += '='
        method_args += f'"{task[argument]}"'
        method_args += ','

    command += method_args
    command += ')'

    return command


async def run_task(task: Dict[str, Any]) -> None:
    apis = task['Platforms'].split(',')
    for api in apis:
        if api not in api_to_function:
            log.error(f'The function keys were: {api_to_function.keys()}')
            log.error(f'{api} is not a valid api.')
            continue

        if api_to_instance[api] is None:
            log.error(f'The API "{api}" does not have all necessary config files!')
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
            # command = f'loop.run_until_complete({command})'
            command = f'await {command}'

        print(f'Command to be executed: {command}')

        # Run the generated string command directly as python code
        eval(command)  # pylint: disable=W0123


async def process_scheduler_events(tasks: List[Dict[str, Any]]) -> None:
    print('received task:')
    print(tasks)
    for task in tasks:
        await run_task(task)
