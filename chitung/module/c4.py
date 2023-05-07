import asyncio
import math
import random
from datetime import datetime

from graia.amnesia.message import MessageChain, Text
from graiax.shortcut import decorate, listen
from graiax.shortcut.saya import every
from graiax.shortcut.text_parser import MatchRegex
from ichika.client import Client
from ichika.core import Group, Member
from ichika.graia.event import GroupMessage
from ichika.message.elements import At

from chitung.core.decorator import FunctionType, Switch


class _C4FlagStore:
    store: set[int] = set()


@listen(GroupMessage)
@decorate(
    MatchRegex(r"^(?:\/|(?:\/?[Oo][Kk] ?))c4"),
    Switch.check(GroupMessage, FunctionType.LOTTERY),
)
async def c4_handler(client: Client, group: Group, member: Member):
    admins = await client.get_group_admins(group.uin)
    if client.uin not in {x[0] for x in admins}:
        return await client.send_group_message(
            group.uin, MessageChain([Text("七筒目前还没有管理员权限，请授予七筒权限解锁更多功能。")])
        )
    if group.uin in _C4FlagStore.store:
        return await client.send_group_message(
            group.uin, MessageChain([Text("今日的C4已经被触发过啦！请明天再来尝试作死！")])
        )
    members = await client.get_member_list(group.uin)
    if random.random() < 1 / math.sqrt(len(members)):
        await client.mute_group(group.uin, True)
        _C4FlagStore.store.add(group.uin)
        await client.send_group_message(group.uin, MessageChain([Text("中咧！")]))
        await client.send_group_message(
            group.uin,
            MessageChain(
                [
                    At(target=member.uin, display=member.card_name or member.nickname),
                    Text(text=" 成功触发了C4！大家一起恭喜TA！"),
                ]
            ),
        )
        loop = asyncio.get_running_loop()
        loop.call_later(300, asyncio.create_task, _callback(client, group))
    else:
        await client.send_group_message(group.uin, MessageChain([Text("没有中！")]))


async def _callback(client: Client, group: Group):
    await client.mute_group(group.uin, False)


@every(
    24,
    "hour",
    start=datetime(
        year=(_now := datetime.now()).year,
        month=_now.month,
        day=_now.day,
        hour=6,
        minute=0,
        second=0,
        microsecond=0,
    ),
)
async def _cleanup():
    _C4FlagStore.store.clear()
