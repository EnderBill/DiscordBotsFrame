import json, sys, os, datetime,random
import discord, asyncio, typing
from discord import *
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
sys.path.append("..")

with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
    config = json.load(reconfig)
with open('data.json', newline='',mode='r',encoding="utf8") as redata: 
    data = json.load(redata)

##??    進程紀錄
def process_in(
    project: str,
    key    : str,
    text   : str
    )      : 
    print(f'-=-\n-=- {str(datetime.datetime.now())} : {text}\n-=-')
    if not os.path.isfile(f'data\\process_data\\{project}_process.json'):
        with open(f'data\\process_data\\{project}_process.json',mode='w',encoding="utf8") as  process_data:
            process = {
                "Page"     : 1,
                "Page_text": 0
            }
            json.dump(process,process_data,ensure_ascii=False,indent = 4)
    with open(f'data\\process_data\\{project}_process.json', newline='',mode='r',encoding="utf8") as process_data:
        process = json.load(process_data)
        if process['Page_text'] >= 10 :
            process['Page']      += 1
            process['Page_text']  = 0
        Page = f'Page{process["Page"]}'
        if Page not in process:
            process[Page]={}
        process[Page][key]    = text
        process['Page_text'] += 1
        with open(f'data\\process_data\\{project}_process.json', newline='',mode='w',encoding="utf8") as process_data:
            json.dump(process,process_data,ensure_ascii=False,indent = 4)

##??    進程查看
async def process_look(
    ctx,
    project: str,
    page   : int,
    BotName: str
    )      : 
    embed = discord.Embed(
        title       = f' >> 進程查看 !! << ',
        description = f'> 給 {ctx.author.mention}',
        color       = 0xab5bdb,
        timestamp   = datetime.datetime.now()
    )
    if not os.path.isfile(f'data\\process_data\\{project}_process.json'):
        with open(f'data\\process_data\\{project}_process.json',mode='w',encoding="utf8") as  look_data:
            look = {
                "Page"     : 1,
                "Page_text": 0
            }
            json.dump(look,look_data,ensure_ascii=False,indent = 4)
    with open(f'data\\process_data\\{project}_process.json', newline='',mode='r',encoding="utf8") as look_data: 
        look  = json.load(look_data)
        pages = look["Page"]-page+1
        process_in(
                project = 'bot',
                key     = str(datetime.datetime.now()),
                text    = f'{ctx.author.name} ({ctx.author.id}) 查看{project} Page{pages}'
            )
        if page <= 0:
            embed.add_field(
                name   = f'>> 頁數並沒有負數或零 :',
                value  = f'> 請輸入正整數 !!',
                inline = False
            )
        elif ( look["Page"] == 1 and look["Page_text"] == 0 ): 
            embed.add_field(
                name   = f'>> 未找到 {project} 資料 :',
                value  = f'> {project} 資料為空 !!',
                inline = False
            )
        elif page > look["Page"]: 
            embed.add_field(
                name   = f'>> 未找到 {project} 第{page}頁資料 :',
                value  = f'> 只有{look["Page"]}頁 !!',
                inline = False
            )
        else: 
            embed.add_field(
                name   = f'{project}紀錄資料 第{page}頁',
                value  = f'> 有{look["Page"]}頁 !!\n> 共 {(look["Page"]-1)*10+look["Page_text"]} 筆',
                inline = False
            )
            
            for x, y in look[f'Page{pages}'].items(): 
                embed.add_field(
                    name   = f'>> {x}',
                    value  = f'> {y}',
                    inline = False
                )
        embed.set_footer(text=BotName)
        await ctx.send(embed=embed)
            
##??    每日簽到
def fortune_in(
    name: str,
    id  : int,
    )   : 
    today = str(datetime.date.today())
    size  = data["整體運勢"]["size"]
    if not os.path.isfile(f'data\\users_data\\{id}.json'):
        with open(f'data\\users_data\\{id}.json',mode='w',encoding="utf8") as reuser:
            user={}
            user["個人資料"]       = data['users_data']["個人資料"]
            user["個人資料"]["ID"] = id
            json.dump(user,reuser,ensure_ascii=False,indent = 4)
    with open(f'data\\users_data\\{id}.json', newline='',mode='r',encoding="utf8") as reuser:
        user = json.load(reuser)
        if "運勢" not in user["個人資料"]:
            user["運勢"]={}
        if today not in user["個人資料"]["簽到記錄"]:
            process_in(
                    project = 'sign',
                    key     = today,
                    text    = f'{name}({id})已簽到'
                )
            user["個人資料"]["名子"] = name
            user["個人資料"]["簽到記錄"].append(today)
            user["運勢"] = data["users_data"]["運勢"]
            for x in data["users_data"]["運勢"]:
                average = 0
                num     = 0
                for y in data["users_data"]["運勢"][x].keys():
                    if not (y=="整體運勢" or y=="幸運數字" or y=="貴人星座"):
                        fortunes  = random.randint(0,size)
                        average  += fortunes
                        num      += 1
                        user["運勢"][x][y] = fortunes
                user["運勢"][x]["整體運勢"]    = round(average/num)
                user["運勢"]["今日"]["幸運數字"] = random.randint(0,9)
                user["運勢"]["今日"]["貴人星座"] = random.choice(data["constellation"])
            with open(f'data\\users_data\\{id}.json', newline='',mode='w',encoding="utf8") as reuser:
                json.dump(user,reuser,ensure_ascii=False,indent = 4)

##??    運勢查看
async def fortune_look(
    ctx,
    user   : discord.User,
    project: str,
    BotName: str
    )      : 
    print(type(user))
    fortune_in(
        name = ctx.author.name,
        id   = ctx.author.id
        )
    today = str(datetime.date.today())
    embed = discord.Embed(
        title       = f' >> 運勢查看 !! << ',
        description = f'> 給 {ctx.author.mention}',
        color       = 0xab5bdb,
        timestamp   = datetime.datetime.now()
    )
    if not os.path.isfile(f'data\\users_data\\{user.id}.json'):
        embed.add_field(
            name   = f'>> 未發現資料 :',
            value  = f'> {user.mention}',
            inline = False
        )
    else:
        with open(f'data\\users_data\\{user.id}.json', newline='',mode='r',encoding="utf8") as reuser:
            users = json.load(reuser)
            if today not in users["個人資料"]["簽到記錄"]:
                embed.add_field(
                    name   = f'今日未簽到 :',
                    value  = f'> {user.mention}',
                    inline = False
                )
            else:
                embed.add_field(
                    name   = f'{project}運勢 查詢 :',
                    value  = f'> 查詢 {user.mention}',
                    inline = False
                )
                for x, y in users["運勢"][project].items():
                    if  (x=="整體運勢"or x=="外道" or x=="恩典" or x=="怨咒"):
                        embed.add_field(
                            name   = f'{x}',
                            value  = f'> {data[str(x)][str(y)]}',
                            inline = False
                            )
                    elif (x=="幸運數字" or x=="貴人星座"): 
                        embed.add_field(
                            name   = f'{x}',
                            value  = f'> {y}',
                            inline = True
                            )
                    else: 
                        embed.add_field(
                            name   = f'{x}',
                            value  = f'> {data["整體運勢"][str(y)]}',
                            inline = True
                            )
    embed.set_footer(text=BotName)
    process_in(
            project = 'sign',
            key     = str(datetime.datetime.now()),
            text    = f'{ctx.author.name}({ctx.author.id}) 查詢 {user.name}({user.id}) 的{project}運勢'
        )
    await ctx.send(embed=embed)
