import os
import discord
from discord.ext import commands
from json import load, dump
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
guild_propane=int(os.getenv('DISCORD_GUILD_PROPANE'))
commands_wiki=load(open('wiki.json'))
bot=commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'))
guild_emoji={}

def format_emoji(name):
    return '<:{0}:{1}>'.format(name, guild_emoji[name])

@bot.event
async def on_ready():
    guild=bot.get_guild(guild_propane)

    for emoji in guild.emojis:
        guild_emoji[emoji.name]=emoji.id
    # Occasionally run this
    #dump(guild_emoji, open('emoji.json', 'w'))

    print('{0} the {1}, roll out! Entering: {2} (id: {3})'.format(guild.me.display_name, bot.user.name, guild.name, guild.id))

@bot.event
async def on_message(message):
    if message.author==bot.user:
        pass
    
    if 'wotcher' in message.content.lower():
        await message.add_reaction(format_emoji('wotcher'))

    await bot.process_commands(message)

@bot.command()
async def wiki(context, entry):
    await context.send('**{0}:** {1}'.format(entry, commands_wiki.get(entry.lower(), 'Entry does not exist.'))) 


bot.run(token)