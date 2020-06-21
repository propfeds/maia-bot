import discord
from dotenv import load_dotenv
from json import load, dump
import math
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
guild_cfg: Dict[int, dict]={}

math_func_dict: dict={
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
die_regex: str=r'(\d+)?[dD](\d+)([\+\-]\d+)?'
entry_regex: str=r'( ?)([^(\?)]+)'  # Second group is entry
end_whitespace_trim_regex: str=r' +$'
_debug_state: bool=False

# Randorg
randorg_client: RandomOrgClient=RandomOrgClient(os.getenv('RANDORG_API_KEY'))

# Gets a Role object. Uses the index from mapping name->ID->index in dicts.
def get_role_from_name(guild: discord.Guild, name: str) -> discord.Role:
    return guild.roles[role_index[guild.id][role_id[guild.id][name]]]

def get_role_from_id(guild: discord.Guild, id_number: int) -> discord.Role:
    return guild.roles[role_index[guild.id][id_number]]

def format_emoji(guild: discord.Guild, name: str, fallback_id: int=None) ->
Union[str, discord.Emoji]:
    emoji=discord.utils.get(guild.emojis, name=name)
    if not emoji:
        return f'<:{name}:{fallback_id}>'
    return emoji

def gather(guild: discord.Guild, dump_json: bool=False) -> None:
    global emoji_id, role_id, role_index, guild_cfg

    emoji_id[guild.id]={}
    role_id[guild.id]={}
    role_index[guild.id]={}

    if not os.path.exists('data/guilds/{0}/'.format(guild.id)):
        os.mkdir('data/guilds/{0}/'.format(guild.id))

    # Emoji name to ID
    for emoji in guild.emojis:
        emoji_id[guild.id][emoji.name]=emoji.id
    if dump_json:
        with open('data/guilds/{0}/emoji_id.json'.format(guild.id), 'w+'
        ) as json_emoji_id:
            dump(emoji_id[guild.id], json_emoji_id, indent=4)

    # Role name to ID then ID to index (in guild's role list)
    for i, role in enumerate(guild.roles):
        role_id[guild.id][role.name]=role.id
        role_index[guild.id][role.id]=i
    if dump_json:
        with open('data/guilds/{0}/role_id.json'.format(guild.id), 'w+'
        ) as json_role_id:
            dump(role_id[guild.id], json_role_id, indent=4)
        # with open('data/guilds/{0}/role_index.json'.format(guild.id), 'w+')
        # as json_role_index:
            # dump(role_index[guild.id], json_role_index, indent=4)

    # Guild config contains role IDs for Bards, Devs, Lorekeeps, Botkeeps and
    # Mutes. If not found, creates a blank slate so every command would fail
    # intentionally.
    if not os.path.exists('data/guilds/{0}/config.json'.format(guild.id)):
        guild_cfg[guild.id]={
            "roles":
            {
                "botkeep": 0,
                "lorekeep": 0,
                "dev": 0,
                "bard": 0,
                "mute": 0
            }
        }
        with open('data/guilds/{0}/config.json'.format(guild.id), 'w+'
        ) as json_guild_cfg:
            dump(guild_cfg[guild.id], json_guild_cfg, indent=4)
    else:
        with open('data/guilds/{0}/config.json'.format(guild.id), 'r'
        ) as json_guild_cfg:
            guild_cfg[guild.id]=load(json_guild_cfg)
