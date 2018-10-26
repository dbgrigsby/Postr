from unittest.mock import patch
from unittest.mock import MagicMock
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

@pytest.mark.asyncio
async def test_post_text() -> None:
    text = 'test text'
    channel_id = '123'

    with patch('postr.discord_api.Client.send_typing', new=CoroutineMock()) as send_typing:
        with patch('postr.discord_api.Client.send_message', new=CoroutineMock()) as send_message:
            with patch('postr.discord_api.id_to_channel') as mock_id_to_channel:
                mock_id_to_channel.return_value = MagicMock(spec=Channel)
                posted = await discord_api.post_text(channel_id=channel_id, text=text)
                send_typing.assert_called_once_with(mock_id_to_channel.return_value)
                send_message.assert_called_once_with(mock_id_to_channel.return_value, text)
                assert posted
