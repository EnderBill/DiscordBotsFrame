from core.Cog_Extension import * # Cog庫 宣告
class system(Cog_Extension): # Cog庫 繼承 # system 需都相同
    def __init__(self,bot):
        super().__init__(
            bot,
            cog_name = 'EX_Cog', # Cog擴充 檔名
            cog_class= 'auto' # Cog擴充 分類
        )
        self.sign()
        
    ##  指令示範
    @commands.hybrid_command(
            name = "wwping",
            description = ">> 查看延遲 !! <<"
    )
    async def wwping(self,ctx):
        await ctx.send(f'>> 目前延遲 : {round((self.bot.latency)*1000)} 毫秒 Q ! <<')
    ##
    
async def setup(bot):
    await bot.add_cog(system(bot)) # system 需都相同

# system 需都相同 但不限定為 system 可為別的字串
