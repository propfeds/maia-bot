import os
import discord
from discord.ext import commands
from json import load, dump
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
guild_propane=int(os.getenv('DISCORD_GUILD_PROPANE'))
commands_wiki=load(open('wiki.json', encoding='utf-8'))
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
    # dump(guild_emoji, open('emoji.json', 'w'))
    # And / or this
    # guild_roles={}
    # for role in guild.roles:
    #     guild_roles[role.name]=role.id
    # dump(guild_roles, open('roles.json', 'w'))

    print('{0} the {1}, roll out! Entering: {2} (id: {3})'.format(guild.me.display_name, bot.user.name, guild.name, guild.id))

@bot.event
async def on_message(message):
    if message.author==bot.user:
        pass

    if 'wotcher' in message.content.lower():
        await message.add_reaction(format_emoji('wotcher'))

    await bot.process_commands(message)

@bot.command(description='Type entries as arguments to learn about various topics.')
async def wiki(context, *entries):
    for entry in entries:
        response='**{0}'.format(entry)

        if commands_wiki.get(entry.lower()):
            entry_cur=entry

            # Redirecting entries
            while commands_wiki.get(entry_cur)[0]=='>':
                entry_cur=commands_wiki.get(entry_cur)[1:]
                response+=('→{0}'.format(entry_cur))

            response+=(':** {0}'.format(commands_wiki.get(entry_cur)))
        else:
            response+=':** Entry does not exist.'
        await context.send(response)

@bot.command(description='Bards you and unbards you.')
async def bard(context):
    role_bard=discord.utils.get(context.guild.roles, name='Bard')

    if role_bard in context.author.roles:
        await context.author.remove_roles(role_bard, reason="Unbarded by command")
        await context.send("Unbarded!")
    else:
        await context.author.add_roles(role_bard, reason="Barded by command")
        await context.send("Barded!")

bot.run(token)
