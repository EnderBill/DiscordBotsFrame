from core.Cog_Extension import *
####!!!! Bot announcement
class MUOMBots(commands. Bot):
     def __init__(self):
         super().__init__(
             command_prefix = commands. when_mentioned_or(config["start"]["prefix"]),
             help_command = None,
             intents = discord. Intents. all(),
             activity = discord. Game("Start Ing~~~"),
             status = discord.Status.dnd
         )
         self.synced = False
        
####!!!!Bot Name
         self.BotName = "Bot Name"
####!!!!Bot Name

         if not os.path.isfile(f'data\\bot_data\\{self.BotName}.json'):
             with open(f'data\\bot_data\\{self.BotName}.json',mode='w',encoding="utf8") as self_data:
                 redata = {
                     "BotName" : self.BotName
                 }
                 json.dump(redata, self_data, ensure_ascii=False, indent=4)
         with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as self_data:
             self.datas = json.load(self_data)
     async def restart(self):
         os.execv(sys.executable, ['python'] + sys.argv)
     async def stop(self):
         await super(). close()
     async def setup_hook(self):
         self.datas['cogs'] = {}
         self.datas['cogs']['cogs_load'] = {}
         self.datas['cogs']['cogs_unload'] = {}
         with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='w',encoding="utf8") as self_data:
             json.dump(self.datas,self_data,ensure_ascii=False,indent=4)
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         for file_name in os.listdir("./cogs"):
             if file_name.endswith('.py'):
                 cog_name = file_name[:-3]
                 await self.load_extension(f"cogs.{cog_name}")
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as self_data:
             self.datas = json.load(self_data)
         await self. tree. sync()
     async def on_ready(self):
         await self. wait_until_ready()
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         print('-=- Login ID : ', bot.user.id )
         print('-=- login as : ', bot.user )
         print('-=- open time: ', str(datetime.datetime.now()))
         print('-=- Turn on delay: ', round(bot.latency*1000), ' milliseconds !')
         print('-=- directive header : ', config["start"]["prefix"])
         print('-=- initial login status : ', config['start']['status'] )
         print('-=- initial game status : ', config['start']['activity'])
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         owners_num = 0
         print(f'-=- current bot holds : {config["owner"]} ')
         for owners_all in config['owners']:
             owners_num+=1
             print(f'-=- currently exists management: ({owners_num}) {owners_all} ')
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         guilds_num = 0
         with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as datas:
             data_data = json. load(datas)
             data_data["guilds"] = {}
             for guilds_all in bot.guilds:
                 if not os.path.isfile(f'data\\guilds_data\\{guilds_all.id}.json'):
                     with open(f'data\\guilds_data\\{guilds_all.id}.json',mode='w',encoding="utf8") as reguilds:
                         guilds = data['guilds_data']
                         guilds["guild_name"] = str(guilds_all)
                         guilds["guild_id"] = guilds_all.id
                         json.dump(guilds,reguilds,ensure_ascii=False,indent=4)
                 guilds_num += 1
                 data_data["guilds"][str(guilds_all)] = guilds_all.id
                 print(f'-=- current guild : ({guilds_num}) {guilds_all} ')
             with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='w',encoding="utf8") as datas:
                 json.dump(data_data,datas,ensure_ascii=False,indent=4)
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         with open(f'data\\users_data\\{bot.user.id}.json', newline='',mode='r',encoding="utf8") as bot_users:
             user = json. load(bot_users)
        
             for x in user["Fortune"]:
                 print(f'-=- robot {x} fortune :\n-=-')
                 sign_num = 1
                 for y,z in user["Fortune"][x].items():
                     if sign_num < 2:
                         sign_num+=1
                     else:
                         print('-=-')
                         sign_num=0
                        
                     if (y=="lucky number" or y=="constellation of noble person"):
                         print(f'-=- >> {y} : {str(z)}')
                     elif(y=="Heretics" or y=="Grace" or y=="Grudges"):
                         print(f'-=- >> {y} : {data[str(y)][str(z)]}')
                     else:
                         print(f'-=- >> {y} : {data["overall fortune"][str(z)]}')
                 print('-=-')
         print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- =-')
         await bot. change_presence(
             status = config['start']['status'],
             activity = discord. Game(config['start']['activity'])
         )
         if not self. synced:
             self.synced = True
bot = MUOMBots()
####!!!! System Instructions
##!! Expansion Adjustment
@bot.hybrid_command(
         name = "recog",
         description = ">> Expand Adjustment !! <<"
)
@app_commands.choices(
     implement = [
         app_commands. Choice(name="look", value="look"),
         app_commands. Choice(name="load", value="load"),
         app_commands. Choice(name="reload", value="reload"),
         app_commands. Choice(name="unload", value="unload")
     ],
     cogs = [
         app_commands.Choice(name=name[:-3],value=name[:-3]) for name in os.listdir(".\\cogs") if name.endswith('.py')
     ]
)
@app_commands.describe(
     implement = ">> Adjustment method ?? <<",
     cogs = ">> adjustment object ?? <<"
)
async def cog(
     ctx,
     implement: typing. Optional[app_commands. Choice[str]],
     cogs : typing. Optional[app_commands. Choice[str]]
     ) :
     embed = discord. Embed(
             title=f' >> Expand Adjustment !! << ',
             description=f'> to {ctx.author.mention}',
             color = 0xab5bdb,
             timestamp = datetime. datetime. now()
         )
     if ctx.author.id in config['owners'].values() :
         with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data:
             datas = json. load(self_data)
         try:
             implement = implement.value
         except:
             implement = "look"
         try:
             cogs = cogs. value
         except:
             cogs = "(empty)"
         if implement == "load":
             if cogs in datas['cogs']['cogs_load'].keys():
                 cogs = f'Extension "{cogs}" is mounted, please use reload'
             elif os.path.isfile(f'cogs\\{cogs}.py'):
                 await bot.load_extension(f'cogs.{cogs}')
                 if cogs in datas['cogs']['cogs_unload'].keys():
                     del datas['cogs']['cogs_unload'][f"{cogs}"]
                     cogs = f'The extension "{cogs}" has been remounted'
                 else:
                     cogs = f'The extension "{cogs}" is mounted'
             else:
                 cogs = f'Extension "{cogs}" not found'
             embed.add_field(
                 name = f'>> mount:',
                 value = f'>{cogs}',
                 inline = False
             )
            
         elif implement == "reload":
             if cogs in datas['cogs']['cogs_load'].keys():
                 await bot.reload_extension(f'cogs.{cogs}')
                 cogs = f'The extension "{cogs}" has been remounted'
             else:
                 cogs = f'No extension "{cogs}" mount found'
             embed.add_field(
                 name = f'>> for overloading:',
                 value = f'>{cogs}',
                 inline = False
             )
         elif implement == "unload":
             if cogs in datas['cogs']['cogs_load'].keys():
                 await bot.unload_extension(f'cogs.{cogs}')
                 datas['cogs']['cogs_unload'][f"{cogs}"] = datas['cogs']['cogs_load'][f"{cogs}"]
                 del datas['cogs']['cogs_load'][f"{cogs}"]
                 cogs = f'The extension "{cogs}" has been unloaded'
             else:
                 cogs = f'No extension "{cogs}" mount found'
             embed.add_field(
                 name = f'>> uninstall:',
                 value = f'>{cogs}',
                 inline = False
             )
         with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='w',encoding="utf8") as self_data:
             json.dump(datas, self_data, ensure_ascii=False, indent=4)
         with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data:
             datas = json. load(self_data)
             out=""
             for cogs, classes in datas['cogs']['cogs_load'].items():
                 out += f'> {classes} : {cogs}\n'
             if out == "" :
                 out = "."
             embed.add_field(
                 name = f'>>mounted:',
                 value = f'{out}',
                 inline = False
             )
             out=""
             for cogs, classes in datas['cogs']['cogs_unload'].items():
                 out += f'> {classes} : {cogs}\n'
             if out == "" :
                 out = "."
             embed.add_field(
                 name = f'>>Unmounted:',
                 value = f'{out}',
                 inline = False
             )
         await ctx. send(embed=embed)
         await bot. tree. sync()
         print(f'-=- {str(datetime.datetime.now())} command reloaded')
     else:
         embed.add_field(
             name = f'>> Insufficient permissions:',
             value = f'> needs robot owner permission',
             inline = False
         )
         embed.set_footer(text=bot.BotName)
         await ctx. send(embed=embed)
##!! status Adjustment
@bot.hybrid_command(
         name = "restart",
         description = ">> status Adjustment !! <<"
)
@app_commands.choices(
     restart = [
         app_commands.Choice(name="restart", value=1),
         app_commands.Choice(name="Do not restart", value=0)
     ],
     status = [
         app_commands.Choice(name=name,value=value) for name, value in data['bot_data']['status'].items()
     ],
     setstart = [
         app_commands.Choice(name="replace initial state", value=1),
         app_commands.Choice(name="do not change the initial state", value=0)
     ]
)
@app_commands.describe(
     restart = ">> Restart ?? <<",
     status = ">> Replace the usage status ?? <<",
     activities = ">> Change game play ?? <<",
     setstart = ">> Replace the initial state ?? <<",
     prefix = ">> replace command header ?? <<"
)
async def restart(
     ctx,
     restart : typing. Optional[app_commands. Choice[int]],
     status : typing. Optional[app_commands. Choice[str]],
     activities: typing. Optional[str],
     setstart : typing. Optional[app_commands. Choice[int]],
     prefix : typing. Optional[str]
     ) :
     embed = discord. Embed(
             title = f' >> state adjustment !! << ',
             description = f'> give {ctx.author.mention}',
             color = 0xab5bdb,
             timestamp = datetime. datetime. now()
         )
     if ctx.author.id in config['owners'].values() :
         with open('config.json', newline='',mode='r',encoding="utf8") as start_config:
             reconfig = json. load(start_config)
         try:
             restart = restart.value
         except:
             restart = 1
         try:
             set_start = setstart.value
         except:
             set_start = 0
         try:
             status = status. value
         except:
             status = config['start']['status']
         if activities != None:
             activities = activities
         else:
             activities = config['start']['activity']
         if prefix != None:
             prefix = prefix
         else:
             prefix = config['start']['prefix']
         embed.add_field(
             name = f'>>use state:',
             value = f'>{status}',
             inline = False
         )
         embed.add_field(
             name = f'>> directive header:',
             value = f'>{prefix}',
             inline = False
         )
         embed.add_field(
             name = f'>> play game:',
             value = f'>{activities}',
             inline = False
         )
         embed.add_field(
             name = f'>>Overwrite initial boot data:',
             value = f'> yes ' if set_start else '> no ',
             inline = False
         )
         embed.add_field(
             name = f'>>restart:',
             value = f'> yes ' if restart else '> no ',
             inline = False
         )
         embed.set_footer(text=bot.BotName)
         await bot. change_presence(
             status = status,
             activity = discord. Game(activities)
         )
         if set_start:
             reconfig['start']['status'] = status
             reconfig['start']['activity'] = activities
         reconfig['start']['prefix'] = prefix
         with open('config.json', newline='',mode='w',encoding="utf8") as start_config:
             json.dump(reconfig, start_config, ensure_ascii=False, indent=4)
         if restart:
             await bot. change_presence(
                 status = discord.Status.dnd,
                 activity = discord.Game('Restart Project')
             )
             await ctx. send(embed=embed)
             bot.synced = False
             await asyncio. sleep(0.1)
             await bot. restart()
         else:
             await ctx. send(embed=embed)
     else:
         embed.add_field(
             name = f'>> Insufficient permissions:',
             value = f'> need robot administrator privileges',
             inline = False
         )
         embed.set_footer(text=bot.BotName)
         await ctx. send(embed=embed)
##!! Stop Execution
@bot.hybrid_command(
         name = "stop",
         description = ">> STOP EXECUTION !! <<"
)
async def stop(ctx):
     embed = discord. Embed(
             title = f' >> stop execution !! << ',
             description = f'> give {ctx.author.mention}',
             color = 0xab5bdb,
             timestamp = datetime. datetime. now()
         )
     if ctx.author.id == config['owner']:
         await bot. change_presence(
             status = discord.Status.offline
         )
         embed.set_footer(text=bot.BotName)
         await ctx. send(embed=embed)
         bot.synced = False
         await asyncio. sleep(1)
         await bot. stop()
     else:
         embed.add_field(
             name = f'>> Insufficient permissions:',
             value = f'> needs robot owner permission',
             inline=False
         )
         embed.set_footer(text=bot.BotName)
         await ctx. send(embed=embed)
##!! View Delay
@bot.hybrid_command(
         name = "ping",
         description = ">> View Delay !! <<"
)
async def ping(ctx):
     embed = discord. Embed(
             title = f' >> View Delay !! << ',
             description = f'> give {ctx.author.mention}',
             color = 0xab5bdb,
             timestamp = datetime. datetime. now()
         )
     embed.add_field(
         name = f'>>current delay: ',
         value = f'> {round((bot.latency)*1000)} milliseconds !!',
         inline = False
     )
     embed.set_footer(text=bot.BotName)
     await ctx. send(embed=embed)
####!!!!    starting program
bot.run(os.getenv(bot.BotName))