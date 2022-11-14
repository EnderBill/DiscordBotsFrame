import json, sys, os, datetime
import discord, asyncio, typing
from discord import *
from discord.ext import commands
from discord.ext.commands import Cog
from dotenv import load_dotenv
load_dotenv()
sys.path.append("..")

class Cog_Extension(commands.Cog):
    def __init__(
            self,
            bot,
            cog_name : str,
            cog_class: str
        ):
        self.bot       = bot
        self.cog_name  = cog_name
        self.cog_class = cog_class
        with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
            self.config = json.load(reconfig)
        with open('data.json', newline='',mode='r',encoding="utf8") as datas:
            self.data = json.load(datas)
    def sign(self):
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
            self.datas['cogs']['cogs_load'][f'{self.cog_name}'] = self.cog_class
            with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='w',encoding="utf8") as self_data: 
                json.dump(self.datas,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
        print(f'-=- 已載入 Cog : {self.cog_class} - {self.cog_name}')