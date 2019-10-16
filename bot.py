import discord
from discord.ext import commands
from dotenv import load_dotenv
from json import load, dump
import os
from random import randint
from rdoclient_py3 import RandomOrgClient, RandomOrgSendTimeoutError, RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError

load_dotenv()
# Discourse
commands_wiki=load(open('data/wiki.json', encoding='utf-8'))
bot=commands.Bot(command_prefix=os.getenv('DISCORD_COMMAND_PREFIX'))
guild_emoji={}
guild_role_indexes={}
# Randorg
randorg_client=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

def get_role(guild, name):
    return guild.roles[guild_role_indexes[name]]

def format_emoji(name):
    return '<:{0}:{1}>'.format(name, guild_emoji[name])

@bot.event
async def on_ready():
    guild=bot.get_guild(int(os.getenv('DISCORD_GUILD_ID')))

    for emoji in guild.emojis:
        guild_emoji[emoji.name]=emoji.id

    for i, role in enumerate(guild.roles):
        guild_role_indexes[role.name]=i

    # Occasionally run this for data observation
    # dump(guild_emoji, open('data/exported/emoji.json', 'w'))
    # And / or this
    # guild_roles={}
    # for role in guild.roles:
    #     guild_roles[role.name]=role.id
    # dump(guild_roles, open('data/exported/roles.json', 'w'))
    # Also this
    # dump(guild_role_indexes, open('data/exported/role_indexes.json', 'w'))

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
    if get_role(context.guild, 'Bard') in context.author.roles:
        await context.author.remove_roles(get_role(context.guild, 'Bard'), reason="Unbarded by command")
        await context.send("Unbarded!")
    else:
        await context.author.add_roles(get_role(context.guild, 'Bard'), reason="Barded by command")
        await context.send("Barded!")

@bot.command(description='Powered by Random.org. Rolls dice with the xdy+m format. First word in reason can specify number of repeats.')
async def roll(context, die, *reason):
    nof_repeats=1
    response="Rolling `{0}`".format(die)
    for i, word in enumerate(reason):
        if not i:
            if word.isdigit():
                nof_repeats=int(word)
                response+=' {0} times for'.format(word)
            else:
                response+=' once for {0}'.format(word)
        else:
            response+=' {0}'.format(word)
    response+=':'
    # Replacing 'd' and '+' with spaces
    die_list=die.translate({100:32, 43:32}).split()
    die_list.append('0')
    dice, sides, mod=int(die_list[0]), int(die_list[1]), int(die_list[2])

    results_dice=[]
    try:
        results_dice.extend(randorg_client.generate_integers(dice*nof_repeats, 1, sides))
    except RandomOrgSendTimeoutError:
        response+='\nRandom.org timeout.'
    except (RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError):
        response+='\nRandom.org out of juice! Using pseudo RNG.'
        for _ in range(dice*nof_repeats):
            results_dice.append(randint(1, sides))
    # Actually displaying dice
    for i in range(nof_repeats):
        roll=results_dice[dice*i:dice*(i+1)]
        response+='\n`{0}`→{1}'.format(str(roll), sum(roll)+mod)

    await context.send(response)



bot.run(os.getenv('DISCORD_TOKEN'))

# Todo: !gungeon @mention time_hours reason: Muted!