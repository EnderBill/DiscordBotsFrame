import json, sys, os, datetime
import discord
from discord import *
import random

with open('MUOMBots\\config.json', newline='',mode='r',encoding="utf8") as reconfig: 
    config = json.load(reconfig)
with open('MUOMBots\\data\\data.json', newline='',mode='r',encoding="utf8") as redata: 
    data = json.load(redata)
with open('MUOMBots\\data\\reload_data.json', newline='',mode='r',encoding="utf8") as set_reload_data: 
    reload_data = json.load(set_reload_data)

##??    進程紀錄
def process_in(
    project: str,
    text   : str
):
    if not os.path.isfile(f'MUOMBots\\data\\process_data\\{project}_process.json'):
        with open(f'MUOMBots\\data\\process_data\\{project}_process.json',mode='w',encoding="utf8") as  process_data:
            process = {
                "Page" : 1,
                "Page_text" : 0
            }
            json.dump(process,process_data,ensure_ascii=False,indent = 4)
    with open(f'MUOMBots\\data\\process_data\\{project}_process.json', newline='',mode='r',encoding="utf8") as process_data:
        process = json.load(process_data)
        if ("Page" or "Page_text") not in process:
            process = {
                "Page" : 1,
                "Page_text" : 0
            }
        if process['Page_text']>=10 :
            process['Page_text'] = 0
            process['Page'] += 1
            Page = f'Page{ process["Page"] }'
        else:
            Page = f'Page{ process["Page"] }'
        if Page not in process:
            process[Page]={}
        process[Page][str(datetime.datetime.now())] = text
        process['Page_text'] += 1
        with open(f'MUOMBots\\data\\process_data\\{project}_process.json', newline='',mode='w',encoding="utf8") as process_data:
            json.dump(process,process_data,ensure_ascii=False,indent = 4)

##??    進程查看
async def process_look(
    interaction: discord.Interaction,
    project: str,
    page   : int,
    text   : str
):
    global process
    process_in('bot',f'{interaction.user.name} ({interaction.user.id}) 查看{project} Page{page}')
    if not os.path.isfile(f'MUOMBots\\data\\process_data\\{project}_process.json'):
        with open(f'MUOMBots\\data\\process_data\\{project}_process.json',mode='w',encoding="utf8") as  process_data:
            process = {
                "Page" : 1,
                "Page_text" : 0
            }
            json.dump(process,process_data,ensure_ascii=False,indent = 4)
    with open(f'MUOMBots\\data\\process_data\\{project}_process.json', newline='',mode='r',encoding="utf8") as process_data:
        process = json.load(process_data)
        if page <= 0:
            await interaction.response.send_message(f'>> 頁數並沒有負數或零 !! <<')
        elif page > process["Page"]:
            await interaction.response.send_message(f'>> 未找到 {text}進程 第{page}頁資料 只有{process["Page"]}頁 !! <<')
        else:
            embed=discord.Embed(
                title=f'{text}進程紀錄資料 第{page}頁', 
                description=f'由 {interaction.user.mention} 查詢', 
                color = 0x00ff80,
                timestamp = datetime.datetime.now()
            )
            for x, y in reversed(process[f'Page{process["Page"]-page+1}'].items()):
                embed.add_field(name=f'>> {x}', value=f'>> {y}',inline=False)
            embed.add_field(name='目前資料量 :', value=f' {(process["Page"]-1)*10+process["Page_text"]} 筆',inline=False)
            embed.set_footer(text=f'by.時蝕的助手')
            await interaction.response.send_message(embed=embed)
            
##??    每日簽到
def sign_in(
    name: str,
    id  : int,
):
    today=str(datetime.date.today())
    size=reload_data["users_data"]["運勢"]["size"]
    if not os.path.isfile(f'MUOMBots\\data\\users_data\\{id}.json'):
        with open(f'MUOMBots\\data\\users_data\\{id}.json',mode='w',encoding="utf8") as reuser:
            user={}
            user["個人資料"] = reload_data['users_data']["個人資料"]
            user["個人資料"]["ID"] =id
            json.dump(user,reuser,ensure_ascii=False,indent = 4)
    with open(f'MUOMBots\\data\\users_data\\{id}.json', newline='',mode='r',encoding="utf8") as reuser:
        user = json.load(reuser)
        if "運勢" not in user["個人資料"]:
            user["運勢"]={}
        if today not in user["個人資料"]["簽到記錄"]:
            process_in('sign',f'{name}({id}) 已簽到')
            user["個人資料"]["名子"] = name
            user["個人資料"]["簽到記錄"].append(today)

            for x in reload_data["users_data"]["運勢"]:
                if x!="size" :
                    user["運勢"][x] = reload_data["users_data"]["運勢"][x]
                    average = 0 
                    num = reload_data["users_data"]["運勢"][x]["整體運勢"] + 1
                    for y in reload_data["users_data"]["運勢"][x]:
                        if  (y=="整體運勢" or y=="幸運數字" or y=="貴人星座"):
                            num -= 1
                        else :
                            fortunes = random.randint(0,size)
                            average += fortunes
                            user["運勢"][x][y] = fortunes
                    user["運勢"][x]["整體運勢"] = round(average/num)
            user["運勢"]["今日"]["幸運數字"] = random.randint(0,9)
            user["運勢"]["今日"]["貴人星座"] = random.choice(data["constellation"])
                
            with open(f'MUOMBots\\data\\users_data\\{id}.json', newline='',mode='w',encoding="utf8") as reuser:
                json.dump(user,reuser,ensure_ascii=False,indent = 4)

##??    運勢查看
async def fortune_look(
    interaction: discord.Interaction,
    users       : discord.User,
    project    : str
):
    sign_in(interaction.user.name,interaction.user.id)
    today=str(datetime.date.today())
    if not os.path.isfile(f'MUOMBots\\data\\users_data\\{users.id}.json'):
        await interaction.response.send_message(f'>> 未發現 {users.mention} 的資料 <<')
    else:
        with open(f'MUOMBots\\data\\users_data\\{users.id}.json', newline='',mode='r',encoding="utf8") as reuser:
            user = json.load(reuser)
            if today not in user["個人資料"]["簽到記錄"]:
                await interaction.response.send_message(f'>> {users.mention} 今日未簽到 <<')
            else:
                embed=discord.Embed(
                    title=f'{users.name} 的 {project}運勢', 
                    description=f'給 {interaction.user.mention} ', 
                    color=0x4f0ba2,
                    timestamp = datetime.datetime.now()
                )
                for x, y in user["運勢"][project].items():
                    if  (x=="整體運勢"):
                        embed.add_field(name=x, value=data["fortune"][str(y)],inline=False)
                    elif  (x=="幸運數字" or x=="貴人星座"):
                        embed.add_field(name=x, value=str(y), inline=True)
                    else :
                        embed.add_field(name=x, value=data["fortune"][str(y)],inline=True)
                embed.set_footer(text="by.時蝕的助手")
                await interaction.response.send_message(embed=embed)
    process_in('sign',f'{interaction.user.name}({interaction.user.id}) 查詢 {users.name}({users.id}) 的{project}運勢')

 