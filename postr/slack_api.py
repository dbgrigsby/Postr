from slackclient import SlackClient
from postr.config import get_api_key

slack_token = get_api_key('Slack', 'API_TOKEN')
default_channel = get_api_key('Slack', 'default_channel')
sc = SlackClient(slack_token)
print(sc.api_call('channels.list', exclude_archived=1))
sc.api_call('chat.postMessage', channel=default_channel, text='Hello from Python! :tada:')
