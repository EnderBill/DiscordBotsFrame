from .function import *
class Cog_Extension(commands.Cog):
    def __init__(
            self,
            bot,
            cog_name : str,
            cog_class: str
        ):
        self.config    = config
        self.data      = data
        self.bot       = bot
        self.cog_name  = cog_name
        self.cog_class = cog_class
        
    def sign(self):
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
            self.datas['cogs']['cogs_load'][f'{self.cog_name}'] = self.cog_class
            with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='w',encoding="utf8") as self_data: 
                json.dump(self.datas,self_data,ensure_ascii=False,indent = 4)
        with open(f'data\\bot_data\\{self.bot.BotName}.json', newline='',mode='r',encoding="utf8") as self_data: 
            self.datas = json.load(self_data)
        print(f'-=- 已載入 Cog : {self.cog_class} - {self.cog_name}')