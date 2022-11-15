from core.Cog_Extension import *
class everyday(Cog_Extension):
    def __init__(self,bot):
        super().__init__(
            bot,
            cog_name = 'everyday', 
            cog_class= 'auto'
        )
        self.sign()
    @commands.hybrid_command(
        name        = "運勢",
        description = ">> 每日運勢 !! <<"
    )
    @app_commands.choices(
        project = [
            app_commands.Choice(name=name,value=name) for name in data["users_data"]["運勢"].keys()
        ]
    )
    @app_commands.describe(
        project = ">> 運勢項目 ?? <<",
        user    = ">> 查詢對象 ?? <<"
    )
    async def fortune(
        self,
        ctx,
        project: typing.Optional[app_commands.Choice[str]],
        user   : typing.Optional[discord.User]
        )      :
        try: 
            project = project.value
        except: 
            project = "今日"
        try:
            await fortune_look(
                ctx     = ctx,
                user    = user,
                project = project,
                BotName = self.bot.BotName
                )
        except:
            await fortune_look(
                ctx     = ctx,
                user    = ctx.author,
                project = project,
                BotName = self.bot.BotName
                )

    @commands.hybrid_command(
        name        = "運勢對應",
        description = ">> 運勢等級對應 !! <<"
    )
    async def fortune_rank(self,ctx):
        txt = ""
        out = ""  
        embed = discord.Embed(
            title       = f' >> 運勢對應 !! << ',
            description = f'> 給 {ctx.author.mention}',
            color       = 0xab5bdb,
            timestamp   = datetime.datetime.now()
        )
        for x,y in data["fortune"].items() :
            if x != 'size':
                if  txt == y:
                    out += f' {x}.'
                else :
                    txt  = y
                    out += f'\n> {txt} : {x}.'
        embed.add_field(
            name=f'級別 ( 0 ~ {data["fortune"]["size"]})',
            value= out,
            inline=False
            )
        for x in data["users_data"]["運勢"] :
            out=f'數量 : {data["users_data"]["運勢"][x]["整體運勢"]}筆\n分別為 :'
            for y in data["users_data"]["運勢"][x].keys() :
                if y!="整體運勢" :
                    out += f'\n> {y}.'
            embed.add_field(
                name=f'運勢-{x}:',
                value= out,
                inline=True
                )
        embed.set_footer(text=self.bot.BotName)
        process_in(
            project = 'sign',
            key     = str(datetime.datetime.now()),
            text    = f'{ctx.author.name}({ctx.author.id}) 查詢 運勢對應'
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name        = "簽到",
        description = ">> 簽到操作 !! <<"
    )
    @app_commands.choices(
        project = [
            app_commands.Choice(name="每日",value="每日"),
            app_commands.Choice(name="查詢",value="查詢")
        ]
    )
    @app_commands.describe(
        project = ">> 運勢項目 ?? <<",
        user    = ">> 查詢對象 ?? <<"
    )
    async def sign_look(
        self,
        ctx,
        project: typing.Optional[app_commands.Choice[str]],
        user   : typing.Optional[discord.User]
        ):
        try: 
            project = project.value
        except: 
            project = "每日"
        embed = discord.Embed(
            title       = f' >> {project}運勢 !! << ',
            description = f'> 給 {ctx.author.mention}',
            color       = 0xab5bdb,
            timestamp   = datetime.datetime.now()
        )
        if project == "每日":
            try: 
                fortune_in(
                    name = user.name,
                    id   = user.id
                    )
                process_in(
                        project = 'sign',
                        key     = str(datetime.date.today()),
                        text    = f'{ctx.author.name}({ctx.author.id}) 已幫 {user.name}({user.id})簽到'
                    )
                embed.add_field(
                    name   = f'{ctx.author.name}({ctx.author.id}) 已幫',
                    value  = f'> {user.name}({user.id})簽到',
                    inline = False
                    )
                
            except: 
                fortune_in(
                    name = ctx.author.name,
                    id   = ctx.author.id
                    )
                embed.add_field(
                    name   = f'每日簽到',
                    value  = f'> {ctx.author.name}({ctx.author.name})已完成',
                    inline = False
                    )
        try:
            name = user.name
            id   = user.id
            if not os.path.isfile(f'data\\users_data\\{id}.json'):
                embed.add_field(
                    name   = f'{name}({id})',
                    value  = f'> 檔案未存在',
                    inline = False
                    )
            else:
                with open(f'data\\users_data\\{id}.json', newline='',mode='r',encoding="utf8") as reuser: 
                    users = json.load(reuser)
                    out=""
                    for i in reversed(users["個人資料"]["簽到記錄"]): 
                        out += f'> {i}\n'                
                    embed.add_field(
                        name   = f'{name}({id})的簽到列表',
                        value  = out,
                        inline = False
                        )
        except: 
            name = ctx.author.name
            id   = ctx.author.id
            if not os.path.isfile(f'data\\users_data\\{id}.json'):
                embed.add_field(
                    name   = f'{name}({id})',
                    value  = f'> 檔案未存在',
                    inline = False
                    )
            else:
                with open(f'data\\users_data\\{id}.json', newline='',mode='r',encoding="utf8") as reuser: 
                    users = json.load(reuser)
                    out=""
                    for i in reversed(users["個人資料"]["簽到記錄"]): 
                        out += f'> {i}\n'                
                    embed.add_field(
                        name   = f'{name}({id})的簽到列表',
                        value  = out,
                        inline = False
                        )
        process_in(
            project = 'sign',
            key     = str(datetime.datetime.now()),
            text    = f'{ctx.author.name}({ctx.author.id}) 查詢 {name}({id})的簽到列表'
        )
        embed.set_footer(text=self.bot.BotName)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(everyday(bot))