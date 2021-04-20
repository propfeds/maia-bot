import discord
from dotenv import load_dotenv
from json import load, dump
import math
import os
from random import randint
from rdoclient import RandomOrgClient
from typing import List, Dict, Tuple, Union

load_dotenv()
# Discourse
with open('data/config.json', encoding='utf-8') as json_config:
    _cfg=load(json_config)
with open('data/responses.json', encoding='utf-8') as json_responses:
    _resp=load(json_responses)
with open('data/wiki.json', encoding='utf-8') as json_wiki:
    _wiki=load(json_wiki)
_guild_cfg: Dict[int, dict]={}
_debug_state: bool=False

_math_func_dict: dict={
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

def roll_array(batch_size: int, sides: int) -> Tuple[List[int], str]:
    err_resp: str=''
    try:
        results: List[int]=_rdo.generate_integers(batch_size, 1, sides)
    except RandomOrgSendTimeoutError:
        err_resp.append(resp['roll']['rdo_timeout']+'\n')
    except (RandomOrgInsufficientRequestsError,
    RandomOrgInsufficientBitsError):
        err_resp.append(resp['roll']['rdo_juice']+'\n')
        results: List[int]=[]
        for _ in range(batch_size):
            results.append(randint(1, sides))
    return results, err_resp
    

def get_cfg(guild: discord.Guild) -> None:
    global _guild_cfg

    if not os.path.exists('data/guilds/'):
        os.mkdir('data/guilds/')

    # Guild config contains role IDs for Lorekeeps, Botkeeps and Mutes. If not
    # found, creates a blank slate so every command would fail intentionally.
    if not os.path.exists(f'data/guilds/{guild.id}.json'):
        _guild_cfg[guild.id]: Dict[str, int]={
            'botkeep': 0,
            'lorekeep': 0,
            'mute': 0
        }
        with open(f'data/guilds/{guild.id}.json', 'w+') as json_guild_cfg:
            dump(_guild_cfg[guild.id], json_guild_cfg, indent=4)
    else:
        with open(f'data/guilds/{guild.id}.json', 'r') as json_guild_cfg:
            _guild_cfg[guild.id]=load(json_guild_cfg)
