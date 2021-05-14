import discord
from dotenv import load_dotenv
from json import dump, load
import os
from random import randint
from rdoclient import RandomOrgClient
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

_cmd=load_cfg('commands')
_resp=load_cfg('responses')
_global=load_cfg('global')
_guild: Dict[int, Dict[str, int]]={}

# Randorg
load_dotenv()
_rdo: RandomOrgClient=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

def get_role(guild: discord.Guild, id_num: int) -> discord.Role:
    return discord.utils.get(guild.roles, id=id_num)

def get_emoji(guild: discord.Guild, name: str, fallback_id: int=None) -> Union[
    str, discord.Emoji]:
    emoji: discord.Emoji=discord.utils.get(guild.emojis, name=name)
    if not emoji:
        return f'<:{name}:{fallback_id}>'
    return emoji

def load_guild_cfg(guild: discord.Guild) -> None:
    global _guild

    if not os.path.exists('data/guilds/'):
        os.mkdir('data/guilds/')

    # Guild config contains role IDs for Lorekeeps, Botkeeps and Mutes. If not
    # found, creates a blank slate so every command would fail intentionally.
    _guild[guild.id]=load_cfg(f'guilds/{guild.id}', {
        'botkeep': 0,
        'lorekeep': 0,
        'mute': 0
    })

def get_possessive(self, noun: str) -> str:
    if noun[-1]=='s':
        return noun+'\''
    else:
        return noun+'\'s'