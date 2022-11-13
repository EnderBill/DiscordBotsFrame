import json, sys, os, datetime
import discord
from discord import *

from dotenv import load_dotenv
load_dotenv()
import math
import random

from function import *
####!!!!



####!!!!    機器人宣告
class MUOMBots(discord.Client):
    def __init__(self):
        super().__init__(
            intents = discord.Intents.all(),
            activity = discord.Game("啟動ing~~~"),            
            status = discord.Status.dnd
        )
        self.synced = False
        
    def restart(self): 
        os.execv(sys.executable, ['python'] + sys.argv)
    async def stop(self):
        await super().close()

    async def on_ready(self):
        await self.wait_until_ready()
        print('\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('-=- 登入ID   : ', client.user.id )
        print('-=- 登入身份 : ', client.user )
        print('-=- 初始登入狀態 : ', config['restatuses'] )
        print('-=- 初始遊玩狀態 : ', config['reactivities'])
        print('-=- 開啟時間 : ', str(datetime.datetime.now()))
        print('-=- 開啟延遲 : ', round(client.latency*1000), ' 毫秒 !')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        owners_num = 0 
        for owners_all in config['owners']:
            owners_num+=1
            print(f'-=- 目前存在管理 : ({owners_num}) {owners_all} ')

        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        guilds_num = 0 
        with open('self_data.json', newline='',mode='r',encoding="utf8") as datas:
            data_data = json.load(datas)
            data_data["guilds"] = {}
            for guilds_all in client.guilds:
                if not os.path.isfile(f'MUOMBots\\data\\guilds_data\\{guilds_all.id}.json'):
                    with open(f'MUOMBots\\data\\guilds_data\\{guilds_all.id}.json',mode='w',encoding="utf8") as reguilds:
                        guilds = reload_data['guilds_data']
                        guilds["guild_name"] = str(guilds_all)
                        guilds["guild_id"] = guilds_all.id                        
                        json.dump(guilds,reguilds,ensure_ascii=False,indent = 4)
                guilds_num  += 1
                data_data["guilds"][str(guilds_all)] = guilds_all.id
                print(f'-=- 目前加入公會 : ({guilds_num}) {guilds_all} ')
            with open('self_data.json', newline='',mode='w',encoding="utf8") as datas:
                json.dump(data_data,datas,ensure_ascii=False,indent = 4)
                
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        
        sign_in(client.user.name,client.user.id)
        with open(f'MUOMBots\\data\\users_data\\{client.user.id}.json', newline='',mode='r',encoding="utf8") as bot_users:
            user = json.load(bot_users)
        
            for x in user["運勢"]:
                print(f'-=- 機器人{x}運勢 :\n-=-')
                sign_num = 1
                for y,z in user["運勢"][x].items():
                    if sign_num < 2:
                        sign_num+=1
                    else:
                        print('-=-')
                        sign_num=0
                    if not (y=="幸運數字" or y=="貴人星座"):
                        print(f'-=- >> {y} : {data["fortune"][str(z)]}')
                    else :  
                        print(f'-=- >> {y} : {str(z)}')
                print('-=-')
                    
          
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')

        statuses = {
            '線上' : discord.Status.online,
            '閒置' : discord.Status.idle,
            '勿擾' : discord.Status.dnd,
            '隱形' : discord.Status.offline
        }
        await client.change_presence(
            activity=discord.Game(config['reactivities']),            
            status = statuses[config['restatuses']]
        )
        process_in('bot',f'{client.user}已完成啟動')
        if not self.synced:
            await slash.sync() 
            self.synced = True

client = MUOMBots()
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
    ],
    start = [
    app_commands.Choice(name="更換初始狀態", value=1),
    app_commands.Choice(name="不更換初始狀態", value=0)
    ]
    )
@app_commands.describe(
    choices = ">> 使用的狀態 ?? <<",
    activities = ">> 遊玩的遊戲 ?? <<"  
)
async def restatuses(
    interaction: discord.Interaction,
    choices    : app_commands.Choice[str],
    activities : str,
    start      : app_commands.Choice[int]
):
    statuses_value = choices.value
    start_value    = start.value
    statuses = {
        '線上': discord.Status.online,
        '閒置': discord.Status.idle,
        '勿擾': discord.Status.dnd,
        '隱形': discord.Status.offline
    }
    if interaction.user.id in config['owners'].values() :
        await client.change_presence(
            status = statuses[statuses_value],
            activity=discord.Game(activities)
        )
        out='狀態'
        if start_value:
            with open('MUOMBots\\config.json', newline='',mode='r',encoding="utf8") as start_reconfig:
                EX_config = json.load(start_reconfig) 
                EX_config["restatuses"] = str(statuses_value)
                EX_config["reactivities"] = str(activities)
                with open('MUOMBots\\config.json', newline='',mode='w',encoding="utf8") as start_reconfig:
                    json.dump(EX_config,start_reconfig,ensure_ascii=False,indent = 4)
            out+='及初始啟動狀態'
        out+=f'更換成"{statuses_value}"並遊玩"{activities}"'
        
        process_in('bot',out)
        await interaction.response.send_message(f'>> {out} !! <<')
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
        await client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game('重啟計畫')
        )
        process_in('bot',f'{client.user}開始重新啟動')
        await interaction.response.send_message(">> 重新啟動 !! <<")
        await client.restart()
    else:
        await interaction.response.send_message(">> 權限不足 !! <<")
        

##!!    停止執行
@slash.command(
        name = "stop",
        description = ">> 停止執行 !! <<"
)
async def stop(
    interaction : discord.Interaction
):
    if interaction.user.id == 518361466139574278:
        process_in('bot',f'{client.user}停止執行')
        await client.change_presence(
            status=discord.Status.offline
        )
        await interaction.response.send_message(">> 停止執行 !! <<")
        await client.stop()
    else:
        await interaction.response.send_message(">> 權限不足 !! <<")
####!!!!



####!!!!    進程紀錄

##!!    系統進程
@slash.command(
    name = "進程_系統",
    description = ">> 查看系統進程 !! <<"
)
@app_commands.describe(
    page = ">> 查看頁數 !! <<"
)
async def bot_process_look(
    interaction: discord.Interaction,
    page   : int
):
    project = "bot"
    text = "系統"
    await process_look(interaction,project,page,text)


##!!    簽到進程
@slash.command(
    name = "進程_簽到",
    description = ">> 查看簽到進程 !! <<"
)
@app_commands.describe(
    page = ">> 查看頁數 !! <<"
)
async def sign_process_look(
    interaction: discord.Interaction,
    page   : int
):
    project = "sign"
    text = "簽到"
    await process_look(interaction,project,page,text)
####!!!!




####!!!!!    RPG運勢

##!!    運勢對應
@slash.command(
    name = "運勢_對應",
    description = ">> 運勢等級對應 !! <<"
)
async def fortune_txt(
    interaction : discord.Interaction,
):
    txt = ""
    out = ""  
    
    embed=discord.Embed(
        title="運勢_對應", 
        description=f'給  {interaction.user.mention}', 
        color=0x4a0bc3,
        timestamp = datetime.datetime.now()
    )
    
    for x,y in data["fortune"].items() :
        if txt == y :
            out += f' {x}.'
        else :
            txt = y
            out += f'\n{txt} : {x}.'
    embed.add_field(name=f'級別 ( 0 ~ {reload_data["users_data"]["運勢"]["size"]})', value= out, inline=False)
    
    for x in reload_data["users_data"]["運勢"] :
        out=""
        if x != "size":
            for y,z in reload_data["users_data"]["運勢"][x].items() :
                if y=="整體運勢" :
                    out += f'數量 : {z}筆\n分別為 : \n'
                else:
                    out += f' {y}.'
            embed.add_field(name=f'運勢_{x}', value= out, inline=False)
    
    embed.set_footer(text="by.時蝕的助手")

    await interaction.response.send_message(embed=embed)

##!!    運勢_今日
@slash.command(
    name = "運勢_今日",
    description = ">> 今日運勢 ?! <<"
)
async def fortune_today(
    interaction: discord.Interaction
):
    await fortune_look(interaction,interaction.user,'今日')    


##!!    運勢
@slash.command(
    name = "運勢",
    description = ">> 來抽取今日運勢吧 !! <<"
)
@app_commands.choices(
    project = [
    app_commands.Choice(name="今日", value="今日"),
    app_commands.Choice(name="戰鬥", value="戰鬥"),
    app_commands.Choice(name="生產", value="生產"),
    app_commands.Choice(name="製造", value="製造")
    ]
)
@app_commands.describe(
    project=">> 什麼項目 ?? <<"
)
async def fortune(
    interaction: discord.Interaction,
    project:app_commands.Choice[str]
):
    await fortune_look(interaction,interaction.user,project.value)
    
##!!    他人運勢
@slash.command(
    name = "運勢_他人",
    description = ">> 其他人今日運勢 ?! <<"
)
@app_commands.choices(
    project = [
    app_commands.Choice(name="今日", value="今日"),
    app_commands.Choice(name="戰鬥", value="戰鬥"),
    app_commands.Choice(name="生產", value="生產"),
    app_commands.Choice(name="製造", value="製造")
    ]
)
@app_commands.describe(
    user = ">> 你想看誰的 ?? <<",
    project=">> 什麼項目 ?? <<"
)
async def fortune_other(
    interaction: discord.Interaction,
    user: discord.User,
    project:app_commands.Choice[str]
):
    await fortune_look(interaction,user,project.value)    


##!!    查看簽到
@slash.command(
    name = "簽到_查看",
    description = ">> 查看簽到紀錄 !! <<"
)
async def sign_look(
    interaction : discord.Interaction
):
    sign_in(interaction.user.name,interaction.user.id)
    with open(f'MUOMBots\\data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
        users = json.load(reuser)
        out=f'以下為 {interaction.user.mention} 的簽到記錄 :\n'
        for i in reversed(users["個人資料"]["簽到記錄"]):
            out+=f'>>{i}\n'
        await interaction.response.send_message(out)     

##!!    查看他人簽到
@slash.command(
    name = "簽到_查看_他人",
    description = ">> 查看他人簽到紀錄 !! <<"
)
@app_commands.describe(
    user = ">> 你想看誰的紀錄 ?? <<"  
)
async def sign_look_other(
    interaction : discord.Interaction,
    user: discord.User
):
    if not os.path.isfile(f'MUOMBots\\data\\users_data\\{user.id}.json'):
        await interaction.response.send_message(f'>> 未發現 "{user.mention}" 的資料 <<')  
    else:
        process_in('sign',f'{interaction.user.name}({interaction.user.id}) 查詢 {user.name}({user.id}) 的紀錄')
        with open(f'MUOMBots\\data\\users_data\\{user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
            users = json.load(reuser)
            out=f'以下為 {user.mention} 的簽到記錄 :\n'
            for i in reversed(users["個人資料"]["簽到記錄"]):
                out+=f'>> {i}\n'
            await interaction.response.send_message(out)    

##!!    簽到
@slash.command(
    name = "簽到",
    description = ">> 每日簽到 !! <<"
)
async def sign(
    interaction : discord.Interaction
):
    sign_in(interaction.user.name,interaction.user.id)
    await interaction.response.send_message(f'>> {interaction.user.mention} 已簽到 !! <<') 

##!!    幫他人簽到
@slash.command(
    name = "簽到_他人",
    description = ">> 幫他人簽到 !! <<"
)
@app_commands.describe(
    user = ">> 你想幫誰簽到 ?? <<"  
)
async def sign_other(
    interaction : discord.Interaction,
    user: discord.User
):
    sign_in(user.name,user.id)
    process_in('sign',f'{interaction.user.name}({interaction.user.id}) 已幫 {user.name}({user.id}) 簽到')
    await interaction.response.send_message(f'>> 已幫 {user.mention} 簽到 !! <<')


####!!!!!


####!!!!!    啟動指令

token = os.getenv("TOKEN_beta")
client.run(
    token,
    reconnect = True
)