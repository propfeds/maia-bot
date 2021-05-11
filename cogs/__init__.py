import discord
from dotenv import load_dotenv
from json import dump, load
import math
import os
from random import randint
from rdoclient import RandomOrgClient
from typing import Callable, Dict, Union

load_dotenv()
# Discourse
with open('data/commands.json', encoding='utf-8') as json_config:
    _cmd=load(json_config)
with open('data/responses.json', encoding='utf-8') as json_responses:
    _resp=load(json_responses)
with open('data/wiki.json', encoding='utf-8') as json_wiki:
    _wiki=load(json_wiki)
_guild_cmd: Dict[int, Dict[str, int]]={}

_math_func_dict: Dict[str, Callable]={
    'ceil': math.ceil, 'comb': math.comb, 'copysign': math.copysign,
    'abs': math.fabs, 'factorial': math.factorial, 'floor': math.floor,
    'fmod': math.fmod, 'frexp': math.frexp, 'fsum': math.fsum, 'gcd': math.gcd,
    'isclose': math.isclose, 'isfinite': math.isfinite, 'isinf': math.isinf,
    'isnan': math.isnan, 'isqrt': math.isqrt, 'ldexp': math.ldexp,
    'modf': math.modf, 'perm': math.perm, 'prod': math.prod,
    'remainder': math.remainder, 'trunc': math.trunc, 'exp': math.exp,
    'expm1': math.expm1, 'log': math.log, 'log1p': math.log1p,
    'log2': math.log2, 'log10': math.log10, 'pow': math.pow, 'sqrt': math.sqrt,
    'acos': math.acos, 'asin': math.asin, 'atan': math.atan,
    'atan2': math.atan2, 'cos': math.cos, 'dist': math.dist,
    'hypot': math.hypot, 'sin': math.sin, 'tan': math.tan,
    'degrees': math.degrees, 'radians': math.radians, 'acosh': math.acosh,
    'asinh': math.asinh, 'atanh': math.atanh, 'cosh': math.cosh,
    'sinh': math.sinh, 'tanh': math.tanh, 'erf': math.erf, 'erfc': math.erfc,
    'gamma': math.gamma, 'lgamma': math.lgamma, 'pi': math.pi, 'e': math.e,
    'tau': math.tau, 'inf': math.inf, 'nan': math.nan
}
# Randorg
_rdo: RandomOrgClient=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

def get_role(guild: discord.Guild, id_num: int) -> discord.Role:
    return discord.utils.get(guild.roles, id=id_num)

def get_emoji(guild: discord.Guild, name: str, fallback_id: int=None) -> Union[
    str, discord.Emoji]:
    emoji: discord.Emoji=discord.utils.get(guild.emojis, name=name)
    if not emoji:
        return f'<:{name}:{fallback_id}>'
    return emoji

def get_cmd(guild: discord.Guild) -> None:
    global _guild_cmd

    if not os.path.exists('data/guilds/'):
        os.mkdir('data/guilds/')

    # Guild config contains role IDs for Lorekeeps, Botkeeps and Mutes. If not
    # found, creates a blank slate so every command would fail intentionally.
    if not os.path.exists(f'data/guilds/{guild.id}.json'):
        _guild_cmd[guild.id]={
            'botkeep': 0,
            'lorekeep': 0,
            'mute': 0
        }
        with open(f'data/guilds/{guild.id}.json', 'w+') as json_guild_cmd:
            dump(_guild_cmd[guild.id], json_guild_cmd, indent=4)
    else:
        with open(f'data/guilds/{guild.id}.json', 'r') as json_guild_cmd:
            _guild_cmd[guild.id]=load(json_guild_cmd)