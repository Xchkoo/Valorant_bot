from nonebot.permission import SUPERUSER
from nonebot import on_command


matcher = on_command("测试超管", permission=SUPERUSER)




@matcher.handle()
async def matcher_handle():
    await matcher.send("超管命令测试成功")




@matcher.got("key", "超管提问")
async def matcher_got():
    await matcher.send("超管命令 got 成功")