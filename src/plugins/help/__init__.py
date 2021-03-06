#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot import on_notice, on_command, on_message
from nonebot import get_driver
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

global_config = get_driver().config


help = on_command(cmd="帮助", aliases={'help'}, priority=10)


# [CQ:at,qq={event.get_user_id()}]
@help.handle()
async def help_handle(event: Event):
    msg = \
        """
    欢迎使用Valorant_bot!
    开源仓库：github.com/Xchkoo/Valorant_bot
    
    
    使用方式： @vb并使用以下命令 有的命令前需加上'/'或'!'。
    普通指令：
    - 帮助
        用法：*可通过qq戳一戳使用此命令*
             @vb /帮助 | help
        说明：显示可用的命令
    - 开黑 
        用法：@vb /开黑 | kaihei | kh <游戏id> <补充信息>
        会自动在机器人加入的群组内转发
        例：
        @vb /开黑 XXX#xxx(游戏id) 3等2 白金局 来能躺的

    一些无聊的命令：
    - 人生重开 
        用法：@vb /人生重开 | remake | liferestart | 人生重来
        说明：人生重开
    - 疯狂星期四
        用法：疯狂星期四
        说明：疯狂星期四
    - 随机唐可可
        用法：/随机唐可可|鲤鱼|鲤鱼王|Liyuu|liyuu <难度：简单|普通|困难|地狱>
        说明：来找到唐可可吧
    - 每日一句
        用法：每日一句
        说明：放点洋屁

    """
    await help.finish(Message(msg))


try:
    from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent
except ImportError:
    pass
else:

    async def _group_poke(event: PokeNotifyEvent) -> bool:
        return event.is_tome()

    group_poke = on_notice(_group_poke, priority=10, block=True)
    group_poke.handle()(help_handle)

    async def _poke(event: PrivateMessageEvent) -> bool:
        return event.sub_type == "friend" and event.message[0].type == "poke"

    poke = on_message(
        _poke,
        priority=10,
    )
    poke.handle()(help_handle)

