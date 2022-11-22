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
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
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
        with open('data\\self_data.json', newline='',mode='r',encoding="utf8") as datas:
            data_data = json.load(datas)
            data_data["guilds"] = {}
            for guilds_all in client.guilds:
                if not os.path.isfile(f'data\\guilds_data\\{guilds_all.id}.json'):
                    with open(f'data\\guilds_data\\{guilds_all.id}.json',mode='w',encoding="utf8") as reguilds:
                        guilds = reload_data['guilds_data']
                        guilds["guild_name"] = str(guilds_all)
                        guilds["guild_id"] = guilds_all.id                        
                        json.dump(guilds,reguilds,ensure_ascii=False,indent = 4)
                guilds_num  += 1
                data_data["guilds"][str(guilds_all)] = guilds_all.id
                print(f'-=- 目前加入公會 : ({guilds_num}) {guilds_all} ')
            with open('data\\self_data.json', newline='',mode='w',encoding="utf8") as datas:
                json.dump(data_data,datas,ensure_ascii=False,indent = 4)
                
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        
        sign_in(client.user.name,client.user.id)
        with open(f'data\\users_data\\{client.user.id}.json', newline='',mode='r',encoding="utf8") as bot_users:
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
                
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')

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
        process_in('bot',str(datetime.datetime.now()),f'{client.user}已完成啟動')
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
            with open('config.json', newline='',mode='r',encoding="utf8") as start_reconfig:
                EX_config = json.load(start_reconfig) 
                EX_config["restatuses"] = str(statuses_value)
                EX_config["reactivities"] = str(activities)
                with open('config.json', newline='',mode='w',encoding="utf8") as start_reconfig:
                    json.dump(EX_config,start_reconfig,ensure_ascii=False,indent = 4)
            out+='及初始啟動狀態'
        out+=f'更換成"{statuses_value}"並遊玩"{activities}"'
        
        process_in('bot',str(datetime.datetime.now()),out)
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
        process_in('bot',str(datetime.datetime.now()),f'{client.user}開始重新啟動')
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
        process_in('bot',str(datetime.datetime.now()),f'{client.user}停止執行')
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
    text = "系統進程"
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
    text = "簽到進程"
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
        if x != "size":
            out=f'數量 : {reload_data["users_data"]["運勢"][x]["整體運勢"]}筆\n分別為 : \n'
            for y,z in reload_data["users_data"]["運勢"][x].items() :
                if y!="整體運勢" :
                    out += f' {y}.'
            
            
            embed.add_field(name=f'運勢_{x}', value= out, inline=False)
    
    embed.set_footer(text="by.爆裂的助手")

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
    with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
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
    if not os.path.isfile(f'data\\users_data\\{user.id}.json'):
        await interaction.response.send_message(f'>> 未發現 "{user.mention}" 的資料 <<')  
    else:
        process_in('sign',str(datetime.datetime.now()),f'{interaction.user.name}({interaction.user.id}) 查詢 {user.name}({user.id}) 的紀錄')
        with open(f'data\\users_data\\{user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
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
    process_in('sign',str(datetime.datetime.now()),f'{interaction.user.name}({interaction.user.id}) 已幫 {user.name}({user.id}) 簽到')
    await interaction.response.send_message(f'>> 已幫 {user.mention} 簽到 !! <<')


####!!!!!



####!!!!!    RPG遊戲

##!!    遊戲開始
@slash.command(
    name = "遊戲_開始",
    description = ">> 開始加入遊戲 !! <<"
)
async def game_open(
    interaction : discord.Interaction
):
    sign_in(interaction.user.name,interaction.user.id)
    with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
        users = json.load(reuser)
        if not "玩家資料" in users:
            
            with open('data\\process_data\\player_process.json', newline='',mode='r',encoding="utf8") as player_process:
                process = json.load(player_process)
                num = (process["Page"]-1)*10+process["Page_text"]+1
                process_in('player',str(interaction.user.id),f'({num}) {interaction.user.name}')
                users["玩家資料"]={
                    "玩家編號" : num
                    }
            with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='w',encoding="utf8") as reuser:
                json.dump(users,reuser,ensure_ascii=False,indent = 4)
            with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
                users = json.load(reuser)
            await interaction.response.send_message(f'>> 遊戲初始化完成, 你好玩家 {users["玩家資料"]["玩家編號"]} !! <<')
        else :
            await interaction.response.send_message(f'>> 你好玩家 {users["玩家資料"]["玩家編號"]} !! <<')     

##!!    遊戲名單
@slash.command(
    name = "遊戲_名單",
    description = ">> 查看遊戲名單 !! <<"
)
@app_commands.describe(
    page = ">> 查看頁數 !! <<"
)
async def sign_process_look(
    interaction: discord.Interaction,
    page   : int
):
    project = "player"
    text = "遊戲名單"
    await process_look(interaction,project,page,text)

# ##!!    職業選擇
# @slash.command(
#     name = "遊戲_職業",
#     description = ">> 選擇職業 !! <<"
# )
# async def game(
#     interaction : discord.Interaction
# ):
#     sign_in(interaction.user.name,interaction.user.id)
#     with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
#         users = json.load(reuser)
#         if "玩家資料" in users:
            
#             users["玩家資料"]={
#                 "玩家職業" : ""
#                 }
#             with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='w',encoding="utf8") as reuser:
#                 json.dump(users,reuser,ensure_ascii=False,indent = 4)
#             with open(f'data\\users_data\\{interaction.user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
#                 users = json.load(reuser)

#             await interaction.response.send_message(f'>> 轉職成功, 玩家 {users["玩家資料"]["玩家編號"]} 職業 {users["玩家資料"]["玩家職業"]} <<')
#         else :
#             await interaction.response.send_message(f'>> 請使用 "\\遊戲_開始" 完成遊戲初始化 !! <<')

####!!!!!



####!!!!!    骰子類指令

##!!    普通骰子
@slash.command(
    name = "dice",
    description = ">> 骰子 !! <<"
)
@app_commands.describe(
    size = ">> 最大值 ?? <<",
    quantity = ">> 執行量 ?? <<"
)
async def dice(
    interaction: discord.Interaction,
    size       : int,
    quantity   : int
):
    ans=[]
    for i in range(quantity):
        ans.append(random.randint(1,size))
    await interaction.response.send_message(f'>> 結果 : {ans} <<')

##!!    餐廳骰子
@slash.command(
    name = "eat",
    description = ">> 吃啥 !! <<"
)
async def eat(
    interaction : discord.Interaction,
):
    with open('data\\eat.json', newline='',mode='r',encoding="utf8") as foods:
        food = json.load(foods)
    ans = random.choice(food['food'])
    await interaction.response.send_message(f'>>  走去吃 : {ans}  <<')

##!!    顯示餐廳
@slash.command(
        name = "eat_show",
        description = ">> 顯示餐廳 !! <<"
)
async def eat_show(
    interaction : discord.Interaction
):  
    with open('data\\eat.json', newline='',mode='r',encoding="utf8") as foods:
        food = json.load(foods)
    await interaction.response.send_message(food['food'])

##!!    增加餐廳
@slash.command(
        name = "eat_add",
        description = ">> 增加餐廳 !! <<"
)
@app_commands.describe(
    add = ">> 加上哪一間 ?? <<"  
)
async def eat_add(
    interaction: discord.Interaction,
    add        : str
):
    with open('data\\eat.json', newline='',mode='r',encoding="utf8") as add_food:
        EX_food = json.load(add_food)
    EX_food['food'].append(add)
    with open('data\\eat.json', newline='',mode='w',encoding="utf8") as add_food:
        json.dump(EX_food,add_food,ensure_ascii=False,indent = 4)
    await interaction.response.send_message(f'>> 新增新餐廳  {add} !! <<')
    print(f'\n>>-=- 由 伺服器端 新增新餐廳  {add} !! -=-<<\n')

##!!    減少餐廳
@slash.command(
        name = "eat_reduce",
        description = ">> 刪除餐廳 !! <<"
)
@app_commands.describe(
    reduce  = ">> 刪除哪一間 ?? <<"  
)
async def eat_reduce(
    interaction: discord.Interaction,
    reduce     : str
):
    with open('data\\eat.json', newline='',mode='r',encoding="utf8") as foods:
        food = json.load(foods)
    if reduce in food['food']:
        with open('data\\eat.json', newline='',mode='r',encoding="utf8") as reduce_food:
            EX_food = json.load(reduce_food)
        EX_food['food'].remove(reduce)
        with open('data\\eat.json', newline='',mode='w',encoding="utf8") as add_food:
            json.dump(EX_food,add_food,ensure_ascii=False,indent = 4)
        await interaction.response.send_message(f'>> 刪除餐廳  {reduce} !! <<')
        print(f'\n>>-=- 由 伺服器端 刪除餐廳  {reduce} !! -=-<<\n')
        
    else :
        await interaction.response.send_message('>> 無此餐廳 !! <<')
####!!!!!



####!!!!!    計算類指令

##!!    進位轉換
@slash.command(
        name = "數學_進位",
        description = ">> 進位轉換 !! <<"
)
@app_commands.describe(
    r_in  = "輸入數值的進位值(2~36)",
    r_out = "數值輸出的進位值(2~36)",
    r_str = "數值本身的數值串(string)"
)
async def r_convert(
    interaction: discord.Interaction,
    r_in       : int,
    r_out      : int,
    r_str      : str
):        
    if r_in == r_out :
        await interaction.response.send_message(' 請不要叫我做這些無意義的事')
    elif not (r_in >= 2 and r_in <= 36):
        await interaction.response.send_message(' !! 錯誤的輸入進位值 !!')
    elif not (r_out >= 2 and r_out <= 36):
        await interaction.response.send_message(' !! 錯誤的輸出進位值 !!')        
    else :
        ##
        burden = ""
        topic  = r_str.split('.')
        bit   = 0
        ##

        ##
        if topic[0][0] == '-' :
            topic[0] = topic[0][1:]
            burden='-'
        if len(topic) > 1:
            bit = 1 
        ##
                     
        if not ( 
            len(topic) < 3 and 
            topic[0].isalnum() and 
            topic[bit].isalnum()
            ):
            await interaction.response.send_message(' !! 錯誤的數值串 !!')
        
        elif not (
                int(data["number"][max(topic[0])]) <= (r_in-1) and 
                int(data["number"][max(topic[bit])]) <= (r_in-1)
                ):
                await interaction.response.send_message(' !! 最大數字錯誤 !!')
        else :
            ##
            bit=0
            between_list=list("")
            between_int=0
            numerator=""
            denominator=""
            ##
            
            ##
            for i in range(len(topic[0])) :
                between_int=data["number"][topic[0][i]]
                bit+=between_int*math.pow(r_in,len(topic[0])-i-1)
            while(bit!=0):
                between_int=int(bit%r_out)
                between_list.insert(0,data["number"][str(between_int)])
                bit=int((bit-between_int)/r_out)
            integer="".join(map(str, between_list))
            ##
             
            ##          
            if len(topic) == 2 :
                bit_numerator=0
                bit_denominator=0
                ##  取十進位分子
                for i in range(len(topic[1])) :
                    between_int=data["number"][topic[1][i]]
                    bit_numerator=bit*math.pow(r_in,i)+between_int
                ##  取十進位分母
                for i in range(len(topic[1])) :
                    bit_denominator+=math.pow(r_in,i+1)
                ##  約分
                bit, between_int = bit_numerator, bit_denominator
                while between_int>0:
                    bit, between_int = between_int, bit% between_int
                bit_numerator= int(bit_numerator/ bit)
                bit_denominator= int(bit_denominator/bit)
                
                ##  取輸出分子
                while(bit_numerator!=0):
                    between_int=int(bit_numerator%r_out)
                    between_list.insert(0,data["number"][str(between_int)])
                    bit_numerator=int((bit_numerator-between_int)/r_out)
                numerator="".join(map(str, between_list))
                ##  取輸出分母
                while(bit_denominator!=0):
                    between_int=int(bit_denominator%r_out)
                    between_list.insert(0,data["number"][str(between_int)])
                    bit_denominator=int((bit_denominator-between_int)/r_out)
                denominator="".join(map(str, between_list))
            ##
            send =  f'原本為 : {r_str}\n'
            send += f'由 {r_in}進位 轉換成 {r_out}進位 !!\n'
            send += f'結果為 : \n'
            if integer != "":
                send += f' {burden} {integer} '
            if  (integer != "" and numerator != ""):
                send += f'\n 又 \n'
            elif numerator != "" :
                send += f' {burden} '
            if  numerator != "":  
                send += f' {numerator} \n  \\  \n {denominator}'
            if  (integer == "" and numerator == ""):
                send += '0'
            await interaction.response.send_message(send)

##!!    階層運算
@slash.command(
        name = "數學_階層",
        description = ">> 階層運算 !! <<"
)
@app_commands.describe(
    number  = "輸入數值(正整數且上限500)"
)
async def factorial(
    interaction: discord.Interaction,
    number     : int
):
    if number < 0:
        await interaction.response.send_message(' !! 請輸入正整數 !! ')
    if number > 500:
        await interaction.response.send_message(' !! 請輸入小於500的正整數 !! ')
    elif number == 0:
        send =  f'你所求為 : {number}!\n'
        send += f'結果為 : 1'
        await interaction.response.send_message(send)
    else :
        send =  f'你所求為 : {number}!\n'
        send += f'結果為 : {math.factorial(number)}'
        await interaction.response.send_message(send)

####!!!!!



####!!!!!    啟動指令

token = os.getenv("TOKEN_Beta")
client.run(
    token,
    reconnect = True
)