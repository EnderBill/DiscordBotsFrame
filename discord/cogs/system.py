from core.Cog_Extension import *
class system(Cog_Extension):
    def __init__(self,bot):
        super().__init__(
            bot,
            cog_name = 'system', 
            cog_class= 'auto'
        )
        self.sign()
    @commands.hybrid_command(
            name = "wwping",
            description = ">> 查看延遲 !! <<"
    )
    async def wwping(self,ctx):
        await ctx.send(f'>> 目前延遲 : {round((self.bot.latency)*1000)} 毫秒 Q ! <<')

async def setup(bot):
    await bot.add_cog(system(bot))