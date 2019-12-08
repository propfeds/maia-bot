import discord
from dotenv import load_dotenv
from json import load, dump
import os
from rdoclient_py3 import RandomOrgClient

load_dotenv()
# Discourse
with open('data/wiki.json', encoding='utf-8') as json_wiki:
    commands_wiki=load(json_wiki)
with open('data/responses.json', encoding='utf-8') as json_responses:
    responses=load(json_responses)

guild_emoji={}
guild_role_ids={}
guild_role_indexes={}

bard_rare_chance=10
die_regex_pattern='(\\d+)?[dD](\\d+)([\\+\\-]\\d+)?'
gungeoneer_role_name='G\u0318\u031d\u034du\u0324\u0347\u032cn\u0329\u0332\u0320g\u0322\u0355\u0355e\u0356\u0317\u033cone\u0341\u0317\u0339e\u034d\u0326\u032dr\u0330?\u0327\u0339\u0333?\u0319\u0330\u031f'

# Randorg
randorg_client=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

def get_role(guild: discord.Guild, name: str) -> discord.Role:
    return guild.roles[guild_role_indexes[guild.id][guild_role_ids[guild.id][name]]]

def gather(guild: discord.Guild, dump_json=False) -> None:
    global guild_emoji, guild_role_ids, guild_role_indexes

    guild_emoji[guild.id]={}
    guild_role_ids[guild.id]={}
    guild_role_indexes[guild.id]={}

    if not os.path.exists('data/guilds/{0}/'.format(guild.id)):
        os.mkdir('data/guilds/{0}/'.format(guild.id))

    # Emoji name to ID
    for emoji in guild.emojis:
        guild_emoji[guild.id][emoji.name]=emoji.id
    if dump_json:
        with open('data/guilds/{0}/emoji.json'.format(guild.id), 'w+') as json_emoji:
            dump(guild_emoji[guild.id], json_emoji, indent=4)

    # Role name to ID then ID to index (in guild's role list)
    for i, role in enumerate(guild.roles):
        guild_role_ids[guild.id][role.name]=role.id
        guild_role_indexes[guild.id][role.id]=i
    if dump_json:
        with open('data/guilds/{0}/role_ids.json'.format(guild.id), 'w+') as json_role_ids:
            dump(guild_role_ids[guild.id], json_role_ids, indent=4)
        with open('data/guilds/{0}/role_indexes.json'.format(guild.id), 'w+') as json_role_indexes:
            dump(guild_role_indexes[guild.id], json_role_indexes, indent=4)
