#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import get_driver, on_command
from nonebot.plugin import require
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from nonebot.params import Arg, Depends, CommandArg
from .config import Config
import traceback
from sqlite3 import IntegrityError

export = require("nonebot_plugin_navicat")

global_config = get_driver().config
plugin_config = Config.parse_obj(get_driver().config)

kaihei = on_command(
    cmd="开黑", aliases={'kaihei', 'kh'}, priority=10, block=True
)


@kaihei.handle()
async def handle_first_receive(state: T_State, args: Message = CommandArg()):
    plaintext = args.extract_plain_text()
    if plaintext:
        state["kaihei_text"] = plaintext


@kaihei.got("kaihei_text", prompt="请输入广播内容：")
async def handle_group_message(event: Event, bot: Bot, state: T_State, kaihei_text: str = Arg()):
    data = []
    error_msg=[]
    msg = Message(f'[CQ:at,qq={event.get_user_id()}]' + "向全体瓦罗兰特玩家公告：\n") + kaihei_text
    try:
        query = "SELECT * FROM QQGROUP"
        rows = await export.sqlite_pool.fetch_all(query=query)
        for col in rows:
            group_id = col[1]
            data.append("\n" + str(group_id))
            try:
                await bot.send_group_msg(group_id=group_id, message=msg)
            except:
                error_msg.append("无法发送信息至 "+str(group_id)+" 可能被禁言或被风控\n")
    except:
        await add_group.finish("ERROR: "+"数据库错误\n"+traceback.format_exc())
    finally:
        if error_msg:
            await kaihei.finish("公告失败!\n\n失败原因：\n" + error_msg + "\n公告内容：\n" + msg + "\n\n公告群组：" + data)
        else:
            await kaihei.finish("公告完毕!\n\n公告内容：\n" + msg + "\n\n公告群组：" + data)


add_group = on_command(
    cmd="添加群组", rule=to_me(), aliases={'add_group'}, permission=SUPERUSER, priority=2, block=True
)


def parse_int(key: str):
    """解析数字，并将结果存入 state 中"""

    async def _key_parser(
            matcher: Matcher, state: T_State, a_input=Arg(key)
    ):
        print(f"运行 parse_int, key: {key}")
        if isinstance(a_input, int):
            return

        plaintext = input.extract_plain_text()
        if not plaintext.isdigit():
            await matcher.reject_arg(key, "请只输入数字，不然我没法理解呢！")
        state[key] = int(plaintext)

    return _key_parser


@add_group.handle()
async def handle_first_receive(state: T_State, args: Message = CommandArg()):
    plaintext = args.extract_plain_text()
    if plaintext.isdigit():
        state["group_id"] = int(plaintext)


@add_group.got("group_id", prompt="请输入一个群组id", parameterless=[Depends(parse_int("group_id"))])
async def handle_group_message(bot: Bot, group_id: int = Arg()):
    await export.sqlite_pool.connect()
    try:
        query = "INSERT INTO QQGROUP(GROUP_ID) VALUES (:GROUP_ID)"
        values = {"GROUP_ID": group_id}
        await export.sqlite_pool.execute(query=query, values=values)
    except IntegrityError:
        traceback.print_exc()
        await add_group.finish("ERROR: 出现重复群组")
    except:
        await add_group.finish("ERROR: 数据库出现问题")
    try:
        await bot.send_group_msg(group_id=group_id, message="此群已被添加到Valorant_bot开黑叫人服务 若有错误 请管理员联系1524049410")
    except:
        error_msg = "无法对" + str(group_id) + "发送被添加信息 可能被禁言或被风控"
    finally:
        if error_msg:
            await add_group.finish("添加" + str(group_id) + "可能失败\n" + error_msg)
        else:
            await add_group.finish("添加" + str(group_id) + "完毕")


del_group = on_command(cmd="删除群组", aliases={'del_group'}, permission=SUPERUSER, priority=10, block=False)


@del_group.handle()
async def handle_first_receive(state: T_State, args: Message = CommandArg()):
    plaintext = args.extract_plain_text()
    if plaintext.isdigit():
        state["group_id"] = int(plaintext)


@del_group.got("group_id", prompt="请输入一个群组id", parameterless=[Depends(parse_int("group_id"))])
async def handle_group_message(bot: Bot, group_id: int = Arg()):
    await export.sqlite_pool.connect()
    try:
        query = "DELETE FROM QQGROUP WHERE GROUP_ID=:GROUP_ID"
        values = {"GROUP_ID": group_id}
        await export.sqlite_pool.execute(query=query, values=values)
        try:
            await bot.send_group_msg(group_id=group_id, message="此群已从Valorant_bot开黑叫人服务中删除 若有错误 请管理员联系1524049410")
        except:
            error_msg = "无法对" + str(group_id) + "发送被删除信息 可能被禁言或被风控"
    except IntegrityError:
        traceback.print_exc()
        await del_group.finish("ERROR: 数据库中无此群组")
    except:
        await del_group.finish("ERROR: 数据库出现问题")

    await del_group.finish("删除" + str(group_id) + "可能失败\n" + error_msg)


show_group = on_command(cmd="显示群组", aliases={'show_group'}, permission=SUPERUSER, priority=10, block=False)


@show_group.handle()
async def handle_show_group():
    data = []
    try:
        query = "SELECT * FROM QQGROUP"
        rows = await export.sqlite_pool.fetch_all(query=query)
        for col in rows:
            group_id = col[1]
            data.append("群id：" + str(group_id) + '\n')
    except:
        traceback.print_exc()
    await show_group.send(message=Message(data))
    await show_group.finish("报告完毕")
