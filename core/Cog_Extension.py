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
    
class Cog_Extension(commands.Cog):
    def __init__(
            self,
            bot,
            Cog_File_Name : str,
            Cog_Classification: str
        ):
        self.config    = config
        self.data      = data
        self.bot       = bot
        self.Cog_File_Name  = Cog_File_Name
        self.Cog_Classification = Cog_Classification
        
    def sign(self):
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
            self.datas['cogs']['cogs_load'][f'{self.cog_name}'] = self.Cog_Classification
            with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='w',encoding="utf8") as self_data: 
                json.dump(self.datas,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
        print(f'-=- Cog loaded : {self.Cog_Classification} - {self.Cog_File_Name}')