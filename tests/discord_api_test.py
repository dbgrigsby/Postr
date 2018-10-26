from typing import Any
from unittest.mock import patch
import pytest

from asynctest import CoroutineMock
from postr import discord_api
from postr.discord_api import Channel


TEST_CONFIG_FILE = 'postr_config_test.ini'


# @pytest.yield_fixture(autouse=True)
# def reset_test_config_file() -> Generator:
#     config.CONFIG_FILE = TEST_CONFIG_FILE
#     yield
#     os.remove(os.path.join(git_root_dir(), TEST_CONFIG_FILE))
# @patch('postr.discord_api.discord.Client.send_typing', new=Mock(return_value=None))
# @patch('postr.discord_api.discord.Client.send_message', new=Mock(return_value=None))

@patch('postr.discord_api.Channel', spec=Channel)
@pytest.mark.asyncio
async def test_post_text(channel: Any) -> None:
    text = 'test text'

    with patch('postr.discord_api.Client.send_typing', new=CoroutineMock()) as send_typing:
        with patch('postr.discord_api.Client.send_message', new=CoroutineMock()) as send_message:
            posted = await discord_api.post_text(channel=channel.return_value, text=text)
            send_typing.assert_called_once_with(channel.return_value)
            send_message.assert_called_once_with(channel.return_value, text)
            assert posted
