import os
import discord
from discord.ext import commands
from json import load
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
guild_propane=int(os.getenv('DISCORD_GUILD_PROPANE'))
commands_wiki=load(open('wiki.json'))
bot=commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX'))
guild_emoji={}

@bot.event
async def on_ready():
    guild=bot.get_guild(guild_propane)

    for emoji in guild.emojis:
        guild_emoji[emoji.name]=emoji.id
    
    print(f'{bot.user.name}, roll out! Entering {guild.name}(id: {guild.id})')

@bot.event
async def on_message(message):
    if message.author==bot.user:
        pass
    
    if 'wotcher' in message.content.lower():
        await message.add_reaction('<:wotcher:{0}>'.format(guild_emoji['wotcher']))

    await bot.process_commands(message)

@bot.command()
async def wiki(context, entry):
    await context.send('{0}: {1}'.format(entry, commands_wiki[entry.lower()]))

bot.run(token)