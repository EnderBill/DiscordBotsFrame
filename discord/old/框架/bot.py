from dotenv import load_dotenv
load_dotenv()

import discord, sys, os, json
from discord import app_commands
from discord.ext.commands import Bot

####!!!!


####!!!!    全域檔案宣告
with open('config.json', newline='',mode='r',encoding="utf8") as reconfig:
    config = json.load(reconfig) 
with open('data/data.json', newline='',mode='r',encoding="utf8") as redata:
    data = json.load(redata)
####!!!!



####!!!!    機器人宣告
class aclient(discord.Client):
    def __init__(self):
        super().__init__(
            intents = discord.Intents.all()
        )
        self.synced = False

    def restart(self): 
        os.execv(sys.executable, ['python'] + sys.argv)
    async def stop(self):
        await super().close()

    async def on_ready(self):
        statuses = {
            '線上' : discord.Status.online,
            '閒置' : discord.Status.idle,
            '勿擾' : discord.Status.dnd,
            '隱形' : discord.Status.offline
        }
        await self.wait_until_ready()
        if not self.synced:
            await slash.sync() 
            self.synced = True
        await client.change_presence(
            activity=discord.Game(config['reactivities']),            
            status = statuses[config['restatuses']]
        )
        print('\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('-=- 登入ID   : ', client.user.id )
        print('-=- 登入身份 : ', client.user )
        print('-=- 初始登入狀態 : ', config['restatuses'] )
        print('-=- 初始遊玩狀態 : ', config['reactivities'])
        print('-=- 目前延遲     : ', round(client.latency*1000), ' 毫秒 !')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        owners_num = 0 
        for owners_all in config['owners']:
            owners_num+=1
            print(f'-=- 目前存在管理 : ({owners_num}) {owners_all} ')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        guilds_num = 0 
        for guilds_all in client.guilds:
            guilds_num+=1
            print(f'-=- 目前加入公會 : ({guilds_num}) {guilds_all} ')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n')

client = aclient()
slash = app_commands.CommandTree(client)

####!!!!



####!!!!    系統設定

##!!    查看延遲
@slash.command(
        name = "ping",
        description = ">> 查看延遲 !! <<"
)
async def ping(
    interaction : discord.Interaction
):
    await interaction.response.send_message(f'>> 目前延遲 : {round(client.latency*1000)} 毫秒 ! <<')

##!!    更換狀態
@slash.command(
        name = "restatuses",
        description = ">> 更換狀態 !! <<"
)
@app_commands.choices(
    choices = [
    app_commands.Choice(name="線上", value="線上"),
    app_commands.Choice(name="閒置", value="閒置"),
    app_commands.Choice(name="勿擾", value="勿擾"),
    app_commands.Choice(name="隱形", value="隱形")
    ]
    )
@app_commands.describe(
    activities = ">> 遊玩的遊戲 ?? <<"  
)
async def restatuses(
    interaction : discord.Interaction,
    choices: app_commands.Choice[str],
    activities : str
):
    statuses_value = choices.value
    statuses = {
        '線上' : discord.Status.online,
        '閒置' : discord.Status.idle,
        '勿擾' : discord.Status.dnd,
        '隱形' : discord.Status.offline
    }
    if interaction.user.id in config['owners'].values() :
        await client.change_presence(
            status = statuses[statuses_value],
            activity=discord.Game(activities)
        )
        await interaction.response.send_message(f'>> 狀態已更換成 " {statuses_value} " 並遊玩 " {activities} " !! <<')
        print(f'\n>>-=- 由 伺服器端 更換狀態成 " {statuses_value} " 並遊玩 " {activities} " !! -=-<<\n')

    else:
        await interaction.response.send_message('>> 權限不足 !! <<')

##!!    重新啟動
@slash.command(
        name = "restart",
        description = ">> 重新啟動 !! <<"
)
async def restart(
    interaction : discord.Interaction
):
    
    if interaction.user.id in config['owners'].values() :
        await interaction.response.send_message(">> 重新啟動 !! <<")
        print('\n>>-=- 由 伺服器端 重新啟動 -=-<<\n')
        await client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game('重啟計畫')
        )
        await client.restart()
    else:
        await interaction.response.send_message(">> 權限不足 !! <<")

##!!    更換啟動狀態
@slash.command(
        name = "start_statuses",
        description = ">> 更換啟動狀態 !! <<"
)
@app_commands.choices(
    choices = [
    app_commands.Choice(name="線上", value="線上"),
    app_commands.Choice(name="閒置", value="閒置"),
    app_commands.Choice(name="勿擾", value="勿擾"),
    app_commands.Choice(name="隱形", value="隱形")
    ]
    )
@app_commands.describe(
    activities = ">> 遊玩的遊戲 ?? <<"  
)
async def start_statuses(
    interaction : discord.Interaction,
    choices: app_commands.Choice[str],
    activities : str
):
    statuses_value = choices.value

    if interaction.user.id in config['owners'].values() :
        
        with open('config.json', newline='',mode='r',encoding="utf8") as start_reconfig:
            EX_config = json.load(start_reconfig) 
        EX_config["restatuses"] = str(statuses_value)
        EX_config["reactivities"] = str(activities)
        with open('config.json', newline='',mode='w',encoding="utf8") as start_reconfig:
            json.dump(EX_config,start_reconfig,ensure_ascii=False,indent = 4)
            
        await interaction.response.send_message(f'>> 啟動狀態已更換成 " {statuses_value} " 並遊玩 " {activities} " !! <<')
        print(f'\n>>-=- 由 伺服器端 更換啟動狀態成 " {statuses_value} " 並遊玩 " {activities} " !! -=-<<\n')

    else:
        await interaction.response.send_message('>> 權限不足 !! <<')

##!!    停止執行
@slash.command(
        name = "stop",
        description = ">> 停止執行 !! <<"
)
async def stop(
    interaction : discord.Interaction
):
    if interaction.user.id == 518361466139574278:
        await interaction.response.send_message(">> 停止執行 !! <<")
        print('\n     >>-=- 由 伺服器端 關閉 -=-<<\n')
        await client.change_presence(
            status=discord.Status.offline
        )
        await client.stop()
        await client.stop()
        await client.stop()
        await client.stop()
    else:
        await interaction.response.send_message(">> 權限不足 !! <<")
####!!!!

####!!!!!    啟動指令

token = os.getenv("TOKEN")
client.run(
    token,
    reconnect = True
)