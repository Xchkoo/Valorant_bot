#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# plugin load
nonebot.load_builtin_plugins("echo")
nonebot.load_plugin("nonebot_plugin_gocqhttp")
nonebot.load_plugin("nonebot_plugin_navicat")
nonebot.load_plugin("nonebot_plugin_asoulcnki")
nonebot.load_plugin("nonebot_plugin_remake")
nonebot.load_plugin("nonebot_plugin_crazy_thursday")
nonebot.load_plugin("nonebot_plugin_randomtkk")
nonebot.load_plugin("nonebot_plugin_everyday_en")
nonebot.load_plugins("src/plugins")


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app", access_log=False)
