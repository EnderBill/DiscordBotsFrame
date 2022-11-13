import sys
import os
import json
import datetime
import asyncio
import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
#pip uninstall discord.py，然後pip install py-cord
#pip install discord.py，然後pip install py-cord
class BotsClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('$'), 
            case_insensitive=True,
            intents=discord.Intents.all(),
            activity = discord.Game("啟動ing~~~"),
            status = discord.Status.dnd
        )
        self.synced = False
        self.remove_command('help')
        self.uptime = datetime.datetime.utcnow()
        
        with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
            self.config = json.load(reconfig)
        self.debug_mode = self.config['debug_mode']
        
    async def setup_hook(self):
        for cogs in os.listdir("cogs"):
            if cogs.endswith(".py") and not cogs.startswith('_'):
                extension = cogs[:-3]
                try:
                    await self.load_extension(f"/cogs.{extension}")
                except Exception as e:
                    exc = f'{type(e).__name__}: {e}'
                    print(f'Failed to load extension {extension}\n{exc}')
    def restart(self): 
        os.execv(sys.executable, ['python'] + sys.argv)
    async def stop(self): 
        await super().close()
        
    async def get_default_prefixes(self, bot, message):
        return commands.when_mentioned(self, message)
    
    async def on_ready(self):
        await self.wait_until_ready()
        print('\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('-=- 登入ID   : ', client.get_user )
        print('-=- 登入身份 : ', client.user )
        print('-=- 目前延遲     : ', round(client.latency*1000), ' 毫秒 !')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        owners_num = 0 
        for owners_all in self.config['owners']:
            owners_num+=1
            print(f'-=- 目前存在管理 : ({owners_num}) {owners_all} ')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        guilds_num = 0 
        for guilds_all in client.guilds:
            guilds_num+=1
            print(f'-=- 目前加入公會 : ({guilds_num}) {guilds_all} ')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n')

        statuses = {
            '線上' : discord.Status.online,
            '閒置' : discord.Status.idle,
            '勿擾' : discord.Status.dnd,
            '隱形' : discord.Status.offline
        }
        await client.change_presence(
            activity=discord.Game(self.config['reactivities']),            
            status = statuses[self.config['restatuses']]
        )
        if not self.synced:
            self.synced = True
            
client = BotsClient()
# # slash = app_commands.CommandTree(client)
# with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
#     config = json.load(reconfig)
# ####!!!!    系統設定

##!!    查看延遲
@client.slash_command(
        name = "ping",
        description = ">> 查看延遲 !! <<"
)
async def ping(
    ctx
):
    await ctx.send(f'>> 目前延遲 : {round(client.latency*1000)} 毫秒 ! <<')
    
##!!    停止執行
@client.slash_command(
        name = "stop",
        description = ">> 停止執行 !! <<"
)
async def stop(
    interaction : discord.Interaction
):
    if interaction.user.id == 518361466139574278:
        # with open(f'data/process_data/bot_process.json', newline='',mode='r',encoding="utf8") as sign_process:
        #     sign = json.load(sign_process)
        #     sign[str(datetime.datetime.now())]=f'停止執行'
        #     with open(f'data/process_data/bot_process.json', newline='',mode='w',encoding="utf8") as sign_process:
        #         json.dump(sign,sign_process,ensure_ascii=False,indent = 4)
        await client.change_presence(
            status=discord.Status.offline
        )
        
        await interaction.response.send_message(">> 停止執行 !! <<")
        await client.stop()
    else:
        await interaction.response.send_message(">> 權限不足 !! <<")
####!!!!

# ##!!    更換狀態
# @slash.command(
#         name = "restatuses",
#         description = ">> 更換狀態 !! <<"
# )
# @apc.choices(
#     choices = [
#     apc.Choice(name="線上", value="線上"),
#     apc.Choice(name="閒置", value="閒置"),
#     apc.Choice(name="勿擾", value="勿擾"),
#     apc.Choice(name="隱形", value="隱形")
#     ],
#     start = [
#     apc.Choice(name="更換初始狀態", value=1),
#     apc.Choice(name="不更換初始狀態", value=0)
#     ]  # type: ignore
#     )
# @apc.describe(
#     choices = ">> 使用的狀態 ?? <<",
#     activities = ">> 遊玩的遊戲 ?? <<"  
# )
# async def restatuses(
#     interaction: discord.Interaction,
#     choices    : apc.Choice[str],
#     activities : str,
#     start      : apc.Choice[int]
# ):
#     statuses_value = choices.value
#     start_value    = start.value
#     statuses = {
#         '線上': discord.Status.online,
#         '閒置': discord.Status.idle,
#         '勿擾': discord.Status.dnd,
#         '隱形': discord.Status.offline
#     }
#     if interaction.user.id in config['owners'].values() :
#         await client.change_presence(
#             status = statuses[statuses_value],
#             activity=discord.Game(activities)
#         )
#         out='狀態'
#         if start_value:
#             with open('config.json', newline='',mode='r',encoding="utf8") as start_reconfig:
#                 EX_config = json.load(start_reconfig) 
#                 EX_config["restatuses"] = str(statuses_value)
#                 EX_config["reactivities"] = str(activities)
#                 with open('config.json', newline='',mode='w',encoding="utf8") as start_reconfig:
#                     json.dump(EX_config,start_reconfig,ensure_ascii=False,indent = 4)
#             out+='及初始啟動狀態'
#         out+=f'更換成"{statuses_value}"並遊玩"{activities}"'
#         with open(f'data/process_data/bot_process.json', newline='',mode='r',encoding="utf8") as sign_process:
#             sign = json.load(sign_process)
#             sign[str(datetime.datetime.now())]=out
#             with open(f'data/process_data/bot_process.json', newline='',mode='w',encoding="utf8") as sign_process:
#                 json.dump(sign,sign_process,ensure_ascii=False,indent = 4)
#         await interaction.response.send_message(f'>> {out} !! <<')
#     else:
#         await interaction.response.send_message('>> 權限不足 !! <<')

# ##!!    重新啟動
# @slash.command(
#         name = "restart",
#         description = ">> 重新啟動 !! <<"
# )
# async def restart(
#     interaction : discord.Interaction
# ):
    
#     if interaction.user.id in config['owners'].values() :
#         await client.change_presence(
#             status=discord.Status.dnd,
#             activity=discord.Game('重啟計畫')
#         )
#         with open(f'data/process_data/bot_process.json', newline='',mode='r',encoding="utf8") as sign_process:
#             sign = json.load(sign_process)
#             sign[str(datetime.datetime.now())]=f'開始重新啟動'
#             with open(f'data/process_data/bot_process.json', newline='',mode='w',encoding="utf8") as sign_process:
#                 json.dump(sign,sign_process,ensure_ascii=False,indent = 4)
#         await interaction.response.send_message(">> 重新啟動 !! <<")
#         await client.restart()  # type: ignore
#     else:
#         await interaction.response.send_message(">> 權限不足 !! <<")


# @client.hybrid_group(fallback="get")
# async def tag(ctx, name):
#     await ctx.send(f"Showing tag: {name}")

# @tag.command()
# async def create(ctx, name):
#     await ctx.send(f"Created tag: {name}")

# async def main():
#     # await client.setup_hook()
#     token = str(os.getenv("TOKEN_beta"))
#     async with client:
#         await client.start(token)
# asyncio.run(main())

token = str(os.getenv("TOKEN_beta"))
client.run(token)