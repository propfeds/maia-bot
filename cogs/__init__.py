import discord
from dotenv import load_dotenv
from json import load, dump
import os
from rdoclient_py3 import RandomOrgClient
from typing import Dict

load_dotenv()
# Discourse
with open('data/commands/config.json', encoding='utf-8') as json_config:
    cfg=load(json_config)
with open('data/commands/responses.json', encoding='utf-8') as json_responses:
    resp=load(json_responses)
with open('data/commands/wiki.json', encoding='utf-8') as json_wiki:
    wiki=load(json_wiki)

emoji_id: Dict[int, Dict[str, int]]={}
role_id: Dict[int, Dict[str, int]]={}
role_index: Dict[int, Dict[int, int]]={}

bard_rare_chance: int=10
die_regex: str='(\\d+)?[dD](\\d+)([\\+\\-]\\d+)?'
gungeoneer_role_name: str='G\u0318\u031d\u034du\u0324\u0347\u032cn\u0329\u0332\u0320g\u0322\u0355\u0355e\u0356\u0317\u033cone\u0341\u0317\u0339e\u034d\u0326\u032dr\u0330?\u0327\u0339\u0333?\u0319\u0330\u031f'

# Randorg
randorg_client: RandomOrgClient=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

# Gets a Role object. Uses the index from mapping name->ID->index in dicts.
def get_role(guild: discord.Guild, name: str) -> discord.Role:
    return guild.roles[role_index[guild.id][role_id[guild.id][name]]]

def gather(guild: discord.Guild, dump_json: bool=False) -> None:
    global emoji_id, role_id, role_index

    emoji_id[guild.id]={}
    role_id[guild.id]={}
    role_index[guild.id]={}

    if not os.path.exists('data/guilds/{0}/'.format(guild.id)):
        os.mkdir('data/guilds/{0}/'.format(guild.id))

    # Emoji name to ID
    for emoji in guild.emojis:
        emoji_id[guild.id][emoji.name]=emoji.id
    if dump_json:
        with open('data/guilds/{0}/emoji_id.json'.format(guild.id), 'w+') as json_emoji_id:
            dump(emoji_id[guild.id], json_emoji_id, indent=4)

    # Role name to ID then ID to index (in guild's role list)
    for i, role in enumerate(guild.roles):
        role_id[guild.id][role.name]=role.id
        role_index[guild.id][role.id]=i
    if dump_json:
        with open('data/guilds/{0}/role_id.json'.format(guild.id), 'w+') as json_role_id:
            dump(role_id[guild.id], json_role_id, indent=4)
        # with open('data/guilds/{0}/role_index.json'.format(guild.id), 'w+') as json_role_index:
            # dump(role_index[guild.id], json_role_index, indent=4)
