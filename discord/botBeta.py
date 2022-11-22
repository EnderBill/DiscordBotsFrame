from core.function import *
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
            self.datas = json.load(self_data)
    async def restart(self):
        os.execv(sys.executable, ['python'] + sys.argv)
    async def stop(self):
        await super().close()
    async def setup_hook(self):
        self.datas['cogs']={}
        self.datas['cogs']['cogs_load']={}
        self.datas['cogs']['cogs_unload']={}
        with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='w',encoding="utf8") as self_data: 
            json.dump(self.datas,self_data,ensure_ascii=False,indent = 4)
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        for file_name in os.listdir("./cogs"):
            if file_name.endswith('.py'):
                cog_name = file_name[:-3]
                await self.load_extension(f"cogs.{cog_name}")
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
        await self.tree.sync()
    async def on_ready(self):
        await self.wait_until_ready()
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print('-=- 登入 ID  : ', bot.user.id )
        print('-=- 登入身份 : ', bot.user )
        print('-=- 開啟時間 : ', str(datetime.datetime.now()))
        print('-=- 開啟延遲 : ', round(bot.latency*1000), ' 毫秒 !')
        print('-=- 指令標頭 : ', config["start"]["prefix"])
        print('-=- 初始登入狀態 : ', config['start']['status'] )
        print('-=- 初始遊玩狀態 : ', config['start']['activity'])
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        owners_num = 0 
        print(f'-=- 目前機器人持有 : {config["owner"]} ')
        for owners_all in config['owners']:
            owners_num+=1
            print(f'-=- 目前存在管理 : ({owners_num}) {owners_all} ')
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        guilds_num = 0 
        with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='r',encoding="utf8") as datas:
            data_data = json.load(datas)
            data_data["guilds"] = {}
            for guilds_all in bot.guilds:
                if not os.path.isfile(f'data\\guilds_data\\{guilds_all.id}.json'):
                    with open(f'data\\guilds_data\\{guilds_all.id}.json',mode='w',encoding="utf8") as reguilds:
                        guilds = data['guilds_data']
                        guilds["guild_name"] = str(guilds_all)
                        guilds["guild_id"]   = guilds_all.id
                        json.dump(guilds,reguilds,ensure_ascii=False,indent = 4)
                guilds_num  += 1
                data_data["guilds"][str(guilds_all)] = guilds_all.id
                print(f'-=- 目前加入公會 : ({guilds_num}) {guilds_all} ')
            with open(f'data\\bot_data\\{self.BotName}.json', newline='',mode='w',encoding="utf8") as datas:
                json.dump(data_data,datas,ensure_ascii=False,indent = 4)
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        fortune_in(
            name = bot.user.name,
            id = bot.user.id
        )
        with open(f'data\\users_data\\{bot.user.id}.json', newline='',mode='r',encoding="utf8") as bot_users:
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
                        print(f'-=- >> {y} : {data["整體運勢"][str(z)]}')
                    else :  
                        print(f'-=- >> {y} : {str(z)}')
                print('-=-')
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        process_in(
                project = 'bot',
                key     = str(datetime.datetime.now()),
                text    = f'{bot.user} ({bot.user.id}) 成功啟動'
            )
        await bot.change_presence(
            status = config['start']['Status'],
            activity = discord.Game(config['start']['activity'])
        )
        if not self.synced:
            self.synced = True
bot = MUOMBots()
####!!!!系統指令
##!!    擴充調整
@bot.hybrid_command(
        name        = "recog",
        description = ">> 擴充調整 !! <<"
)
@app_commands.choices(
    implement = [
        app_commands.Choice(name="look", value="look"),
        app_commands.Choice(name="load", value="load"),
        app_commands.Choice(name="reload", value="reload"),
        app_commands.Choice(name="unload", value="unload")
    ],
    cogs = [
        app_commands.Choice(name=name[:-3],value=name[:-3]) for name in os.listdir(".\\cogs") if name.endswith('.py')
    ]
)
@app_commands.describe(
    implement = ">> 進行調整方式 ?? <<",
    cogs      = ">> 調整對象 ?? <<"
)
async def cog(
    ctx,
    implement: typing.Optional[app_commands.Choice[str]],
    cogs     : typing.Optional[app_commands.Choice[str]]
    )        : 
    embed = discord.Embed(
            title=f' >> 擴充調整 !! << ', 
            description=f'> 給 {ctx.author.mention}', 
            color = 0xab5bdb,
            timestamp = datetime.datetime.now()
        )
    if ctx.author.id in config['owners'].values() :
        with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            datas = json.load(self_data)
        try: 
            implement = implement.value
        except: 
            implement = "look"
        try: 
            cogs = cogs.value
        except: 
            cogs = " (空) "    
        if implement == "load":
            if cogs in datas['cogs']['cogs_load'].keys():
                cogs = f'擴充 "{cogs}" 已掛載,請使用 reload'
            elif os.path.isfile(f'cogs\\{cogs}.py'):
                await bot.load_extension(f'cogs.{cogs}')
                if cogs in datas['cogs']['cogs_unload'].keys():
                    del datas['cogs']['cogs_unload'][f"{cogs}"]
                    cogs = f'擴充 "{cogs}" 已重新掛載'
                else:
                    cogs = f'擴充 "{cogs}" 已進行掛載'
            else: 
                cogs = f'未找到擴充 "{cogs}"'
            embed.add_field(
                name   = f'>> 進行掛載 :',
                value  = f'> {cogs}',
                inline = False
            )
            
        elif implement == "reload":
            if cogs in datas['cogs']['cogs_load'].keys():
                await bot.reload_extension(f'cogs.{cogs}')
                cogs = f'擴充 "{cogs}" 已重新掛載'
            else: 
                cogs = f'未找到擴充 "{cogs}" 掛載'
            embed.add_field(
                name   = f'>> 進行重載 :',
                value  = f'> {cogs}',
                inline = False
            )
        elif implement == "unload":
            if cogs in datas['cogs']['cogs_load'].keys():
                await bot.unload_extension(f'cogs.{cogs}')
                datas['cogs']['cogs_unload'][f"{cogs}"] = datas['cogs']['cogs_load'][f"{cogs}"]
                del datas['cogs']['cogs_load'][f"{cogs}"]
                cogs = f'擴充 "{cogs}" 已進行卸載'
            else: 
                cogs = f'未找到擴充 "{cogs}" 掛載'
            embed.add_field(
                name   = f'>> 進行卸載 :',
                value  = f'> {cogs}',
                inline = False
            )
        with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='w',encoding="utf8") as self_data: 
            json.dump(datas,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            datas = json.load(self_data)
            out=""
            for cogs,classes in datas['cogs']['cogs_load'].items():
                out += f'> {classes} : {cogs}\n'
            if out == "" :
                out = "."
            embed.add_field(
                name   = f'>> 已掛載 :',
                value  = f'{out}',
                inline = False
            )
            out=""
            for cogs,classes in datas['cogs']['cogs_unload'].items():
                out += f'> {classes} : {cogs}\n'
            if out == "" :
                out = "."
            embed.add_field(
                name   = f'>> 已卸載 :',
                value  = f'{out}',
                inline = False
            )
        await ctx.send(embed=embed)
        await bot.tree.sync()
        print(f'-=- {str(datetime.datetime.now())} 指令已重新載入')
    else:
        embed.add_field(
            name   = f'>> 權限不足 :',
            value  = f'> 需機器人擁有者權限',
            inline = False
        )
        embed.set_footer(text=bot.BotName)
        await ctx.send(embed=embed)
##!!    狀態調整
@bot.hybrid_command(
        name        = "restart",
        description = ">> 狀態調整 !! <<"
)
@app_commands.choices(
    restart = [
        app_commands.Choice(name="進行重新啟動", value=1),
        app_commands.Choice(name="不進行重新啟動", value=0)
    ],
    status = [
        app_commands.Choice(name=name,value=value) for name, value in data['bot_data']['status'].items()
    ],
    setstart = [
        app_commands.Choice(name="更換初始狀態", value=1),
        app_commands.Choice(name="不更換初始狀態", value=0)
    ]
)
@app_commands.describe(
    restart    = ">> 進行重新啟動 ?? <<",
    status     = ">> 更換使用狀態 ?? <<",
    activities = ">> 更換遊玩遊戲 ?? <<",
    setstart   = ">> 更換初始狀態 ?? <<",
    prefix     = ">> 更換指令標頭 ?? <<"
)
async def restart(
    ctx,
    restart   : typing.Optional[app_commands.Choice[int]],
    status    : typing.Optional[app_commands.Choice[str]],
    activities: typing.Optional[str],
    setstart  : typing.Optional[app_commands.Choice[int]],
    prefix    : typing.Optional[str]
    )         : 
    embed = discord.Embed(
            title       = f' >> 狀態調整 !! << ',
            description = f'> 給 {ctx.author.mention}',
            color       = 0xab5bdb,
            timestamp   = datetime.datetime.now()
        )
    if ctx.author.id in config['owners'].values() :
        with open('config.json', newline='',mode='r',encoding="utf8") as start_config:
            reconfig = json.load(start_config)
        try:
            restart = restart.value
        except:
            restart = 1 
        try:
            set_start = setstart.value
        except:
            set_start = 0
        try:
            Status = status.value
        except:
            Status = config['start']['Status']
        if activities != None:
            activities = activities
        else:
            activities = config['start']['activity']
        if prefix != None:
            prefix = prefix
        else:
            prefix = config['start']['prefix']
        status = data['bot_data']['Status'][Status]
        embed.add_field(
            name   = f'>> 使用狀態 :',
            value  = f'> {status}',
            inline = False
        )
        embed.add_field(
            name   = f'>> 指令標頭 :',
            value  = f'> {prefix}',
            inline = False
        )
        embed.add_field(
            name   = f'>> 遊玩遊戲 :',
            value  = f'> {activities}',
            inline = False
        )
        embed.add_field(
            name   = f'>> 覆蓋初始啟動資料 :',
            value  = f'> 是 ' if set_start else '> 否 ',
            inline = False
        ) 
        embed.add_field(
            name   = f'>> 重新啟動 :',
            value  = f'> 是 ' if restart else '> 否 ',
            inline = False
        )
        embed.set_footer(text=bot.BotName)
        await bot.change_presence(
            status   = Status,
            activity = discord.Game(activities)
        )
        if set_start:
            reconfig['start']['Status']   = Status
            reconfig['start']['status']   = status
            reconfig['start']['activity'] = activities
        reconfig['start']['prefix'] = prefix            
        with open('config.json', newline='',mode='w',encoding="utf8") as start_config:
            json.dump(reconfig,start_config,ensure_ascii=False,indent = 4)
        if restart:
            await bot.change_presence(
                status   = discord.Status.dnd,
                activity = discord.Game('重啟計畫')
            )
            await ctx.send(embed=embed)
            bot.synced = False
            await asyncio.sleep(0.1)
            await bot.restart()
        else:
            await ctx.send(embed=embed)
    else:
        embed.add_field(
            name   = f'>> 權限不足 :',
            value  = f'> 需機器人管理員權限',
            inline = False
        )
        embed.set_footer(text=bot.BotName)
        await ctx.send(embed=embed)
##!!    停止執行
@bot.hybrid_command(
        name        = "stop",
        description = ">> 停止執行 !! <<"
)
async def stop(ctx):
    embed = discord.Embed(
            title       = f' >> 停止執行 !! << ',
            description = f'> 給 {ctx.author.mention}',
            color       = 0xab5bdb,
            timestamp   = datetime.datetime.now()
        )
    if ctx.author.id == config['owner']:
        await bot.change_presence(
            status = discord.Status.offline
        )
        embed.set_footer(text=bot.BotName)
        await ctx.send(embed=embed)    
        bot.synced = False
        await asyncio.sleep(1)
        await bot.stop()
    else:
        embed.add_field(
            name  = f'>> 權限不足 :',
            value = f'> 需機器人擁有者權限',
            inline=False
        )
        embed.set_footer(text=bot.BotName)
        await ctx.send(embed=embed)
##!!    查看延遲
@bot.hybrid_command(
        name        = "ping",
        description = ">> 查看延遲 !! <<"
)
async def ping(ctx):
    embed = discord.Embed(
            title       = f' >> 查看延遲 !! << ',
            description = f'> 給 {ctx.author.mention}',
            color       = 0xab5bdb,
            timestamp   = datetime.datetime.now()
        )
    embed.add_field(
        name   = f'>> 目前延遲 : ',
        value  = f'> {round((bot.latency)*1000)} 毫秒 !!',
        inline = False
    )
    embed.set_footer(text=bot.BotName)
    await ctx.send(embed=embed)
####!!!!    啟動程序
bot.run(os.getenv(bot.BotName))