# Queries: General moderation and information tools.

import asyncio
import cogs
import discord
from discord.ext import commands
from json import dump
from random import randint
import re
from typing import Iterator, Match, Optional

class Queries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    def get_possessive(self, noun: str) -> str:
        if noun[-1]=='s':
            return noun+'\''
        else:
            return noun+'\'s'

    @commands.command(
        aliases=cogs.cfg['define']['aliases'],
        brief=cogs.cfg['define']['brief'],
        description=cogs.cfg['define']['desc'],
        help=cogs.cfg['define']['help'],
        hidden=cogs.cfg['define']['hidden']
    )
    async def define(self, ctx: commands.Context, *entries: str) -> None:
        if cogs._debug_state:
            await ctx.send(cogs.resp['play']['debug_on'])
        entry_full: str=' '.join(entries).lower()
        # Second group in match is entry
        entry_list: Iterator[Match[str]]=re.finditer(r'( ?)([^(\?)]+)',
            entry_full)
        for entry_itr in entry_list:
            entry=entry_itr.group(2)
            # Trim ending whitespace
            entry=re.sub(r' +$', '', entry)
            if not entry:
                continue
            response: str='\n**'+entry

            if cogs.wiki.get(entry):
                # Array entries
                if type(cogs.wiki[entry])==list:
                    response+=':**\n- '
                    response+='\n- '.join(cogs.wiki[entry])
                else:
                    # Redirecting entries
                    while cogs.wiki[entry][0]=='>':
                        entry=cogs.wiki[entry][1:]
                        response+='→'+entry
                    
                    if type(cogs.wiki[entry])==list:
                        response+=':**\n- '
                        response+='\n- '.join(cogs.wiki[entry])
                    else:
                        response+=':** '+cogs.wiki[entry]
            else:
                response+=':** '+cogs.resp['define']['404']

            await ctx.send(response)

# Modes:
# 1: Add (default)
# 0: Add & Modify
# -1: Delete
    @commands.command(
        aliases=cogs.cfg['modifine']['aliases'],
        brief=cogs.cfg['modifine']['brief'],
        description=cogs.cfg['modifine']['desc'],
        help=cogs.cfg['modifine']['help'],
        hidden=cogs.cfg['modifine']['hidden']
    )
    async def modifine(self, ctx: commands.Context, entry: str, mode:
        Optional[int]=1, *value: str) -> None:
        if cogs._debug_state:
            await ctx.send(cogs.resp['play']['debug_on'])
        role_lorekeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild_cfg[ctx.guild.id]['lorekeep'])
        if role_lorekeep not in ctx.author.roles:
            await ctx.send(cogs.resp['modifine']['403'])
            return

        entry=entry.lower()

        if mode==-1:
            if not cogs.wiki.get(entry):
                await ctx.send(cogs.resp['modifine']['404'])
                return

            del cogs.wiki[entry]
            await ctx.send(cogs.resp['modifine']['delete'].format(entry))
            # If not returned, export will commence
        else:
            if not len(value):
                await ctx.send(cogs.resp['modifine']['empty_entry'])
                return

            if cogs.wiki.get(entry) and mode==1:
                await ctx.send(cogs.resp['modifine']['entry_exists'])
                return

            cogs.wiki[entry]=' '.join(value)
            await ctx.send(cogs.resp['modifine']['add_mod'].format(entry))
            # If not returned, export will commence
        with open('data/wiki.json', 'w+', encoding='utf-8'
        ) as json_wiki:
            dump(cogs.wiki, json_wiki, sort_keys=True, indent=4)

    @commands.command(
        aliases=cogs.cfg['mute']['aliases'],
        brief=cogs.cfg['mute']['brief'],
        description=cogs.cfg['mute']['desc'],
        help=cogs.cfg['mute']['help'],
        hidden=cogs.cfg['mute']['hidden']
    )
    async def mute(self, ctx: commands.Context, member: discord.Member,
        hours: str, *reason: str) -> None:
        if cogs._debug_state:
            await ctx.send(cogs.resp['play']['debug_on'])
        if member==self.bot.user or (
            not ctx.author.guild_permissions.manage_roles):
            await ctx.send(cogs.resp['mute']['403'])
            return

        hours_float: float=eval(hours, {"__builtins__": None}, None)
        if hours_float<0:
            await ctx.send(cogs.resp['mute']['negative_duration'])
            return

        role_mute: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild_cfg[ctx.guild.id]['mute'])
        reason_full: str=' '.join(reason)
        response: str=cogs.resp['mute']['mute'].format(member.display_name,
            hours_float, reason_full)
        if member==ctx.author:
            response+=' '+cogs.resp['mute']['self_mute']
        await ctx.send(response)
        await member.add_roles(role_mute, reason=reason_full)

        await asyncio.sleep(hours_float*3600.0)
        response=cogs.resp['mute']['unmute'].format(member.mention,
            hours_float, reason_full)
        if member==ctx.author:
            response+=' '+cogs.resp['mute']['self_mute']
        await ctx.send(response)
        await member.remove_roles(role_mute, reason='Not '+reason_full)

    @commands.command(
        aliases=cogs.cfg['play']['aliases'],
        brief=cogs.cfg['play']['brief'],
        description=cogs.cfg['play']['desc'],
        help=cogs.cfg['play']['help'],
        hidden=cogs.cfg['play']['hidden']
    )
    async def play(self, ctx: commands.Context, *game: str) -> None:
        role_botkeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild_cfg[ctx.guild.id]['botkeep'])
        if role_botkeep not in ctx.author.roles:
            await ctx.send(cogs.resp['play']['403'])
            return

        game_full: str=' '.join(game)

        if game_full=='':
            await ctx.send(cogs.resp['play']['404'])
            return
        elif game_full in ('Debug', 'debug'):
            cogs._debug_state=not cogs._debug_state
            if cogs._debug_state:
                await ctx.send(cogs.resp['play']['debug_on'])
                await self.bot.change_presence(activity=discord.Game('Debug'),
                    status=discord.Status.dnd)
            else:
                await ctx.send(cogs.resp['play']['debug_off'])
                await self.bot.change_presence(activity=None,
                    status=discord.Status.online)
        elif game_full in ('Nothing, nothing'):
            await self.bot.change_presence(activity=None)
            # Export status for use next launch
            with open('data/game.txt', 'w+', encoding='utf-8') as game_cfg:
                game_cfg.write('')
        else:
            if cogs.resp['play'].get(game_full):
                await ctx.send(cogs.resp['play'][game_full])
            await self.bot.change_presence(activity=discord.Game(game_full))
            # Export status for use next launch
            with open('data/game.txt', 'w+', encoding='utf-8') as game_cfg:
                game_cfg.write(game_full)

