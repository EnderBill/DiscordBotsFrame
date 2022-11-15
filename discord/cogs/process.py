from core.Cog_Extension import *
class process(Cog_Extension):
    def __init__(self,bot):
        super().__init__(
            bot,
            cog_name = 'process', 
            cog_class= 'auto'
        )
        self.sign()
    @commands.hybrid_command(
        name = "進程",
        description = ">> 查看進程 !! <<"
    )
    @app_commands.choices(
        project = [
            app_commands.Choice(name=name[:-13],value=name[:-13]) for name in os.listdir("data\\process_data") if name.endswith('.json')
        ]
    )
    @app_commands.describe(
        project = ">> 查看進程 ?? <<",
        page = ">> 查看頁數 ?? <<"
    )
    async def process(
        self,
        ctx,
        project: app_commands.Choice[str],
        page   : int
    ):
        await process_look(
            ctx     = ctx,
            project = project.value,
            page    = page,
            BotName = self.bot.BotName
            )
async def setup(bot):
    await bot.add_cog(process(bot))