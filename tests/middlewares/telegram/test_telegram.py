import json
from pathlib import Path

from nonebug import App
from nonebot.adapters.telegram import Bot, Event
from nonebot.adapters.telegram.model import File
from nonebot.adapters.telegram.config import BotConfig
from nonebot.adapters.onebot.v12 import PrivateMessageEvent

bot_config = BotConfig(token="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI")


async def test_to_onebot_event(app: App):
    from nonebot_plugin_all4one.middlewares.telegram import Middleware

    with (Path(__file__).parent / "updates.json").open("r", encoding="utf8") as f:
        test_updates = json.load(f)

    async with app.test_api() as ctx:
        bot = ctx.create_bot(base=Bot, self_id=bot_config)  # type:ignore
        middleware = Middleware(bot)

        event = Event.parse_event(test_updates[0])
        event = await middleware.to_onebot_event(event)
        assert isinstance(event[0], PrivateMessageEvent)

        event = Event.parse_event(test_updates[3])
        event = await middleware.to_onebot_event(event)
        assert isinstance(event[0], PrivateMessageEvent)
        assert event[0].message[0].type == "reply"

        event = Event.parse_event(test_updates[6])
        ctx.should_call_api(
            "get_file",
            {"file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX"},
            File(file_id="AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", file_unique_id=""),
        )
        event = await middleware.to_onebot_event(event)
        assert isinstance(event[0], PrivateMessageEvent)
        assert event[0].message[0].type == "audio"

        event = Event.parse_event(test_updates[7])
        ctx.should_call_api(
            "get_file",
            {"file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX"},
            File(file_id="AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", file_unique_id=""),
        )
        event = await middleware.to_onebot_event(event)
        assert isinstance(event[0], PrivateMessageEvent)
        assert event[0].message[0].type == "voice"

        event = Event.parse_event(test_updates[8])
        ctx.should_call_api(
            "get_file",
            {"file_id": "AwADBAADbXXXXXXXXXXXGBdhD2l6_XX"},
            File(file_id="AwADBAADbXXXXXXXXXXXGBdhD2l6_XX", file_unique_id=""),
        )
        event = await middleware.to_onebot_event(event)
        assert isinstance(event[0], PrivateMessageEvent)
        assert event[0].message[0].type == "file"