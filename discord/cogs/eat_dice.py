from core.Cog_Extension import *
class eat_dice(Cog_Extension):
    def __init__(self,bot):
        super().__init__(
            bot,
            cog_name = 'eat_dice', 
            cog_class= 'auto'
        )
        self.sign()
    with open('data\\eat.json', newline='',mode='r',encoding="utf8") as reeat: 
        eat = json.load(reeat)
    @commands.hybrid_command(
        name = "eat",
        description = ">> 吃啥 !! <<"
    )
    @app_commands.choices(
        action = [
            app_commands.Choice(name="抽取", value="抽取"),
            app_commands.Choice(name="列表", value="列表"),
            app_commands.Choice(name="增加", value="增加"),
            app_commands.Choice(name="刪除", value="刪除")
        ],
        change = [
            app_commands.Choice(name=name,value=name) for name in eat["food"]
        ]
    )
    @app_commands.describe(
        action = ">> 進行動作 ?? <<",
        change = ">> 變更對象 ?? <<"
    )
    async def eat(
        self,
        ctx,
        action: typing.Optional[app_commands.Choice[str]],
        change: typing.Optional[app_commands.Choice[str]]
    ):
        with open('data\\eat.json', newline='',mode='r',encoding="utf8") as reeat: 
            eat = json.load(reeat)
            try:
                action = action.value
            except:
                action = "抽取"
            try:
                change = change.value
            except:
                change = "餐廳"
            embed = discord.Embed(
                title       = f' >> 餐廳骰子 !! << ',
                description = f'> 給 {ctx.author.mention}',
                color       = 0xab5bdb,
                timestamp   = datetime.datetime.now()
            )
            ans = ""
            if action == "增加":
                if change in eat["food"]:
                    ans = f'不可重複增加'
                else:
                    ans = f'已增加 {change}'
                    eat['food'].append(change)
                embed.add_field(
                    name   = f'>>  增加餐廳 :',
                    value  = f'> {ans}',
                    inline = False
                )  
            if action == "刪除":
                if change not in eat["food"]:
                    ans = f'無此餐廳'
                else:
                    ans = f'已刪除 {change}'
                    eat['food'].remove(change)
                embed.add_field(
                    name   = f'>>  刪除餐廳 :',
                    value  = f'> {ans}',
                    inline = False
                )
            with open('data\\eat.json', newline='',mode='w',encoding="utf8") as reeat:
                json.dump(eat,reeat,ensure_ascii=False,indent = 4)
        with open('data\\eat.json', newline='',mode='r',encoding="utf8") as reeat: 
            eat = json.load(reeat)
            if action == "抽取":
                change = random.choice(eat['food'])
                embed.add_field(
                    name   = f'>>  走去吃 :',
                    value  = f'> {change}',
                    inline = False
                )
            else:
                names=""
                num=0
                for name in eat["food"]:
                    names += f'> {name}\n'
                    num += 1
                
                embed.add_field(
                    name   = f'>>  餐廳列表 : (有{num}間)',
                    value  = f'{names}\n>-',
                    inline = False
                )
            embed.set_footer(text=self.bot.BotName)
            process_in(
                    project = 'eat',
                    key     = str(datetime.datetime.now()),
                    text    = f'餐廳骰子 {ctx.author.name}({ctx.author.id}) {action} {change} {ans}'
                )
            await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(eat_dice(bot))