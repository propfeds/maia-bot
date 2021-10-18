# Json files for command info and stuff

import discord
from json import dump, load
from typing import Dict, Union

# Discourse
def load_cfg(name: str, default_dict: Dict={}) -> Dict:
    try:
        with open(f'data/{name}.json', encoding='utf-8') as f:
            cfg: Dict=load(f)
    except FileNotFoundError:
        cfg=default_dict
        with open(f'data/{name}.json', 'w+') as f:
            dump(cfg, f, indent=4)
    finally:
        return cfg

def get_role(guild: discord.Guild, id_num: int) -> discord.Role:
    return discord.utils.get(guild.roles, id=id_num)

def get_emoji(guild: discord.Guild, name: str, fallback_id: int=None) -> Union[
    str, discord.Emoji]:
    emoji: discord.Emoji=discord.utils.get(guild.emojis, name=name)
    if not emoji:
        return f'<:{name}:{fallback_id}>'
    return emoji

def get_possessive(noun: str) -> str:
    if noun[-1]=='s':
        return noun+'\''
    else:
        return noun+'\'s'

_guild: Dict[int, Dict[str, int]]={}
_cmd=load_cfg('commands')
_resp=load_cfg('responses')
_global=load_cfg('config', {
    'prefixes': ['maia '],
    'autoruns': [],
})
