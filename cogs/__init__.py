import discord
from dotenv import load_dotenv
from json import dump, load
import math
import os
from random import randint
from rdoclient import RandomOrgClient
from typing import Callable, Dict, Union

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
_wiki=load_cfg('wiki')
_global=load_cfg('global')
_guild: Dict[int, Dict[str, int]]={}

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

def get_guild_cfg(guild: discord.Guild) -> None:
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