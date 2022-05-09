from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import get_driver, on_command
from nonebot.plugin import require
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from nonebot.params import Arg, Depends, CommandArg
from nonebot.log import logger
from .config import Config
import traceback
from sqlite3 import IntegrityError
from typing import Union
from uuid import uuid4
from nonebot import get_driver

export = require("nonebot_plugin_navicat")

global_config = get_driver().config
plugin_config = Config.parse_obj(get_driver().config)


class BlackList:
    data = []

    async def fresh(self):
        self.data = []
        try:
            query = "SELECT * FROM BLACKLIST"
            rows = await export.sqlite_pool.fetch_all(query=query)
            for col in rows:
                id = int(col[1])
                self.data.append(id)
        except:
            traceback.print_exc()


b = BlackList()
driver = get_driver()


@driver.on_startup
async def _():
    await b.fresh()


def parse_int(key: str):
    """解析数字，并将结果存入 state 中"""

    async def _key_parser(
            matcher: Matcher, state: T_State, a_input: Union[int, Message] = Arg(key)
    ):
        print(f"运行 parse_int, key: {key}")
        if isinstance(a_input, int):
            return

        plaintext = a_input.extract_plain_text()
        if not plaintext.isdigit():
            await matcher.reject_arg(key, "请只输入数字，不然我没法理解呢！")
        state[key] = int(plaintext)

    return _key_parser


add_blacklist = on_command(cmd="add_blacklist", rule=to_me(), permission=SUPERUSER, priority=10, block=True)


@add_blacklist.handle()
async def _(state: T_State, args: Message = CommandArg()):
    plaintext = args.extract_plain_text()
    if plaintext.isdigit():
        state["id"] = int(plaintext)


@add_blacklist.got("id", "请输入一个需封禁的qq用户id", parameterless=[Depends(parse_int("id"))])
async def _(id: Union[int, str, Message] = Arg()):
    if isinstance(id, Message):
        id = id.extract_plain_text()
    if isinstance(id, str):
        if id.isdigit():
            id = int(id)
        else:
            await add_blacklist.reject("ERROR：qq用户id非正确格式")
            logger.opt(colors=True).error("<y>qq用户id非正确格式</y>")
    try:
        query = "INSERT INTO BLACKLIST(UUID, ID) VALUES (:UUID, :ID)"
        values = {"UUID": str(uuid4()), "ID": id}
        await export.sqlite_pool.execute(query=query, values=values)
    except IntegrityError:
        traceback.print_exc()
        logger.opt(colors=True).error("<y>出现重复qq</y>")
        await add_blacklist.finish("ERROR: 出现重复qq")
    except:
        logger.opt(colors=True).error("<y>数据库出现问题</y>")
        traceback.print_exc()
        await add_blacklist.finish("ERROR: 数据库出现问题")
    await add_blacklist.send("用户" + str(id) + "已被封禁")
    await b.fresh()


del_blacklist = on_command(cmd="del_blacklist", rule=to_me(), permission=SUPERUSER, priority=10, block=True)


@del_blacklist.handle()
async def _(state: T_State, args: Message = CommandArg()):
    plaintext = args.extract_plain_text()
    if plaintext.isdigit():
        state["id"] = int(plaintext)


@del_blacklist.got("id", "请输入一个需解除封禁的qq用户id", parameterless=[Depends(parse_int("id"))])
async def _(id: Union[int, str, Message] = Arg()):
    if isinstance(id, Message):
        id = id.extract_plain_text()
    if isinstance(id, str):
        if id.isdigit():
            id = int(id)
        else:
            await add_blacklist.reject("ERROR：qq用户id非正确格式")
            logger.opt(colors=True).error("<y>qq用户id非正确格式</y>")
    try:
        query = "DELETE FROM BLACKLIST WHERE ID = :ID"
        values = {"ID": id}
        await export.sqlite_pool.execute(query=query, values=values)
    except IntegrityError:
        traceback.print_exc()
        logger.opt(colors=True).error("<y>此用户未被封禁</y>")
        await add_blacklist.finish("ERROR: 此用户未被封禁")
    except:
        logger.opt(colors=True).error("<y>数据库出现问题</y>")
        await add_blacklist.finish("ERROR: 数据库出现问题")
    await del_blacklist.send("用户" + str(id) + "已被解除封禁")
    await b.fresh()


show_blacklist = on_command(cmd="show_blacklist", rule=to_me(), permission=SUPERUSER, priority=10, block=True)


@show_blacklist.handle()
async def _():
    msg = ''
    for user in b.data:
        msg += str(user)+'\n'
    await show_blacklist.finish(message=msg)
