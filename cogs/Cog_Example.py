from core.Cog_Extension import *

# Cog_Example can be changed to any
class Cog_Example(Cog_Extension):
    def __init__(self,bot):
        super().__init__(
            bot,
            # Cog File Name
            Cog_File_Name = 'Cog_Example', 
            # Cog Classification
            Cog_Classification = 'auto'
        )
    # Cog content
async def setup(bot):
    await bot.add_cog(Cog_Example(bot))