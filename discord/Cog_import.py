import json
import discord, asyncio
from discord import *
from discord.ext import commands

with open('config.json', newline='',mode='r',encoding="utf8") as reconfig: 
    config = json.load(reconfig)
with open('data.json', newline='',mode='r',encoding="utf8") as datas: 
    data = json.load(datas)