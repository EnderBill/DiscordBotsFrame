from discord.ext import commands
import os

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    config['prefix']),
    description='')

bot.loaded_cogs = []
bot.unloaded_cogs = []

def check_if_dirs_exist():
    '''Function that creates the "cogs" directory if it doesn't exist already'''
    os.makedirs('cogs', exist_ok=True)

def load_autoload_cogs():
    '''
    Loads all .py files in the cogs subdirectory that are in the config file as "autoload_cogs" as cogs into the bot. 
    If your cogs need to reside in subfolders (ie. for config files) create a wrapper file in the cogs 
    directory to load the cog.
    '''
    for entry in os.listdir('cogs'):
        if entry.endswith('.py') and os.path.isfile('cogs/{}'.format(entry)) and entry[:-3] in config['autoload_cogs']:
            try:
                bot.load_extension("cogs.{}".format(entry[:-3]))
                bot.loaded_cogs.append(entry[:-3])
            except Exception as e:
                print(e)
            else:
                print('Succesfully loaded cog {}'.format(entry))

def get_names_of_unloaded_cogs():
    '''
    Creates an easy loadable list of cogs.
    If your cogs need to reside in subfolders (ie. for config files) create a wrapper file in the auto_cogs
    directory to load the cog.
    '''
    for entry in os.listdir('cogs'):
        if entry.endswith('.py') and os.path.isfile('cogs/{}'.format(entry)) and entry[:-3] not in bot.loaded_cogs:
            bot.unloaded_cogs.append(entry[:-3])

check_if_dirs_exist()
load_autoload_cogs()
get_names_of_unloaded_cogs()

@bot.command()
async def list_cogs(ctx):
    '''Lists all cogs and their status of loading.'''
    cog_list = commands.Paginator(prefix='', suffix='')
    cog_list.add_line('**✅ Succesfully loaded:**')
    for cog in bot.loaded_cogs:
        cog_list.add_line('- ' + cog)
    cog_list.add_line('**❌ Not loaded:**')
    for cog in bot.unloaded_cogs:
        cog_list.add_line('- ' + cog)
    
    for page in cog_list.pages:
        await ctx.send(page)

@bot.command()
async def load(ctx, cog):
    '''Try and load the selected cog.'''
    if cog not in bot.unloaded_cogs:
        await ctx.send('⚠ WARNING: Cog appears not to be found in the available cogs list. Will try loading anyway.')
    if cog in bot.loaded_cogs:
        return await ctx.send('Cog already loaded.')
    try:
        bot.load_extension('cogs.{}'.format(cog))
    except Exception as e:
        await ctx.send('**💢 Could not load cog: An exception was raised. For your convenience, the exception will be printed below:**')
        await ctx.send('```{}\n{}```'.format(type(e).__name__, e))
    else:
        bot.loaded_cogs.append(cog)
        bot.unloaded_cogs.remove(cog)
        await ctx.send('✅ Cog succesfully loaded.')

@bot.command()
async def unload(ctx, cog):
    if cog not in bot.loaded_cogs:
        return await ctx.send('💢 Cog not loaded.')
    bot.unload_extension('cogs.{}'.format((cog)))
    bot.loaded_cogs.remove(cog)
    bot.unloaded_cogs.append(cog)
    await ctx.send('✅ Cog succesfully unloaded.')

@bot.event
async def on_ready():
    print('----------')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('----------')
