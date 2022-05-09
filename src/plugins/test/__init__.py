#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nonebot import on_command
from nonebot.params import Arg, T_State, Message, Matcher, CommandArg, Depends, RawCommand
from typing import Union

test = on_command(cmd='test', priority=10, block=False)


@test.handle()
async def _(state: T_State, args: Message = CommandArg()):
    argsList = args.extract_plain_text().split(' ')
    print(argsList)
    if len(argsList) == 0 or argsList[0] == '':
        return
    elif len(argsList) == 1:
        state["msg1"] = argsList[0]
    elif len(argsList) == 2:
        state["msg1"] = argsList[0]
        state["msg2"] = argsList[1]
    else:
        await test.reject("参数过多")


@test.got("msg1", "输入信息1")
@test.got("msg2", "输入信息2")
async def handle_func(msg1: Union[str, Message] = Arg(), msg2: Union[str, Message] = Arg()):
    await test.finish("msg1:" + msg1 + " msg2:" + msg2)
