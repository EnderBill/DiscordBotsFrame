import json, sys, os, datetime
import discord, asyncio, typing
from discord import *
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
    config = json.load(reconfig)
with open('data.json', newline='',mode='r',encoding="utf8") as datas: 
    data = json.load(datas)
####!!!!Bot宣告
class MUOMBots(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or(config["start"]["prefix"]),
            help_command   = None,
            intents        = discord.Intents.all(),
            activity       = discord.Game(" 啟動 Ing~~~"),
            status         = discord.Status.dnd
        )
        self.synced  = False
        self.BotName = "時蝕的助手"
        if not os.path.isfile(f'data\\bot_data\\{self.BotName}.json'):
            with open(f'data\\bot_data\\{self.BotName}.json',mode='w',encoding="utf8") as self_data:
                redata = {
                    "BotName" : self.BotName
                }
                json.dump(redata,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.data = json.load(self_data)
    async def restart(self):
        os.execv(sys.executable, ['python'] + sys.argv)
    async def stop(self):
        await super().close()
    async def setup_hook(self):
        self.data['cogs']=[]
        for file_name in os.listdir("./cogs"):
            if file_name.endswith('.py'):
                cog_name = file_name[:-3]
                await self.load_extension(f"cogs.{cog_name}")
                self.data['cogs'].append(cog_name)
        with open(f'data\\bot_data\\{client.BotName}.json',mode='w',encoding="utf8") as self_data:
            json.dump(self.data,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{client.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.data = json.load(self_data)
        await self.tree.sync()
    async def on_ready(self):
        await self.wait_until_ready()
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('-=- 登入 ID  : ', client.user.id )
        print('-=- 登入身份 : ', client.user )
        print('-=- 開啟時間 : ', str(datetime.datetime.now()))
        print('-=- 開啟延遲 : ', round(client.latency*1000), ' 毫秒 !')
        print('-=- 指令標頭 : ', config["start"]["prefix"])
        print('-=- 初始登入狀態 : ', config['start']['status'] )
        print('-=- 初始遊玩狀態 : ', config['start']['activity'])        

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        await client.change_presence(
            status = config['start']['Status'],
            activity = discord.Game(config['start']['activity'])
        )
        if not self.synced:
            self.synced = True
client = MUOMBots()
####!!!!
####!!!!系統指令
##!!    查看延遲
@client.hybrid_command(
        name = "ping",
        description = ">> 查看延遲 !! <<"
)
async def ping(ctx):
    embed = discord.Embed(
            title=f' >> 查看延遲 !! << ', 
            description=f' >> 給 {ctx.author.mention}', 
            color = 0xab5bdb,
            timestamp = datetime.datetime.now()
        )
    embed.add_field(name=">> 目前延遲 : ",value=f'>> {round((client.latency)*1000)} 毫秒 !',inline=False)
    embed.set_footer(text=client.BotName)
    await ctx.send(embed=embed)
##!!    更換狀態
@client.hybrid_command(
        name = "restart",
        description = ">> 更換狀態 !! <<"
)
@app_commands.choices(
    restart_value = [
        app_commands.Choice(name="進行重新啟動", value=1),
        app_commands.Choice(name="不進行重新啟動", value=0)
    ],
    status_value = [
        app_commands.Choice(name=name,value=value) for name,value in data['bot_data']['status'].items()
    ],
    set_start_value = [
        app_commands.Choice(name="更換初始狀態", value=1),
        app_commands.Choice(name="不更換初始狀態", value=0)
    ]
)
@app_commands.describe(
    restart_value    = ">> 進行重新啟動 ?? <<",
    status_value     = ">> 更換使用狀態 ?? <<",
    activities_value = ">> 更換遊玩遊戲 ?? <<",
    set_start_value  = ">> 更換初始狀態 ?? <<",
    prefix_value     = ">> 更換指令標頭 ?? <<"
)
async def restart(
    ctx,
    restart_value   : typing.Optional[app_commands.Choice[int]],
    status_value    : typing.Optional[app_commands.Choice[str]],
    activities_value: typing.Optional[str],
    set_start_value : typing.Optional[app_commands.Choice[int]],
    prefix_value    : typing.Optional[str]
):
    embed = discord.Embed(
            title=f' >> 狀態調整 !! << ', 
            description=f' >> 給 {ctx.author.mention}', 
            color = 0xab5bdb,
            timestamp = datetime.datetime.now()
        )
    if ctx.author.id in config['owners'].values() :
        with open('config.json', newline='',mode='r',encoding="utf8") as start_config:
            reconfig = json.load(start_config)
        try:
            restart = restart_value.value
        except:
            restart = 1 
        try:
            set_start = set_start_value.value
        except:
            set_start = 0
        try:
            Status = status_value.value
        except:
            Status = config['start']['Status']
        if activities_value != None:
            activities = activities_value
        else:
            activities = config['start']['activity']
        if prefix_value != None:
            prefix = prefix_value
        else:
            prefix = config['start']['prefix']
            
        status = data['bot_data']['Status'][Status]
        embed.add_field(name=">> 使用狀態 :", value=f'>> {status}',inline=False)
        embed.add_field(name=">> 指令標頭 :", value=f'>> {prefix}',inline=False)
        embed.add_field(name=">> 遊玩遊戲 :", value=f'>> {activities}',inline=False)
        embed.add_field(name=">> 覆蓋初始啟動資料 !! <<",value='>> 是 ' if set_start else '>> 否 ',inline=False) 
        embed.add_field(name=">> 重新啟動 !! <<",value='>> 是 ' if restart else '>> 否 ',inline=False)
        embed.set_footer(text=client.BotName)
        await client.change_presence(
            status = Status,
            activity=discord.Game(activities)
        )
        if set_start:
            reconfig['start']['Status'] = Status
            reconfig['start']['status'] = status
            reconfig['start']['activity'] = activities
        reconfig['start']['prefix'] = prefix            
        with open('config.json', newline='',mode='w',encoding="utf8") as start_config:
            json.dump(reconfig,start_config,ensure_ascii=False,indent = 4)
            
        if restart:
            await client.change_presence(
                status=discord.Status.dnd,
                activity=discord.Game('重啟計畫')
            )
            await ctx.send(embed=embed)
            client.synced = False
            await asyncio.sleep(1)
            await client.restart()
        else:
            await ctx.send(embed=embed)
    else:
        embed.add_field(name=">> 權限不足 :",value='>> 需機器人管理員權限',inline=False)
        embed.set_footer(text=client.BotName)
        await ctx.send(embed=embed)
##!!    停止執行
@client.hybrid_command(
        name = "stop",
        description = ">> 停止執行 !! <<"
)
async def stop(ctx):
    embed = discord.Embed(
            title=f' >> 停止執行 !! << ', 
            description=f' >> 給 {ctx.author.mention}', 
            color = 0xab5bdb,
            timestamp = datetime.datetime.now()
        )
    if ctx.author.id == 518361466139574278:
        await client.change_presence(
            status=discord.Status.offline
        )
        embed.set_footer(text=client.BotName)
        await ctx.send(embed=embed)    
        client.synced = False
        await asyncio.sleep(1)
        await client.stop()
    else:
        embed.add_field(name=">> 權限不足 :",value='>> 需機器人擁有者權限',inline=False)
        embed.set_footer(text=client.BotName)
        await ctx.send(embed=embed)   
####!!!!
####!!!!    啟動程序
client.run(os.getenv("TOKEN_Beta"))