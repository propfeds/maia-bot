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

    @commands.command(**cogs._cmd['define'])
    async def define(self, ctx: commands.Context, *entries: str) -> None:
        if cogs._global['playing']=='Debug':
            await ctx.send(cogs._resp['play']['Debug'])
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

            if cogs._wiki.get(entry):
                # Array entries
                if type(cogs._wiki[entry])==list:
                    response+=':**\n- '
                    response+='\n- '.join(cogs._wiki[entry])
                else:
                    # Redirecting entries
                    while cogs._wiki[entry][0]=='>':
                        entry=cogs._wiki[entry][1:]
                        response+='→'+entry
                    
                    if type(cogs._wiki[entry])==list:
                        response+=':**\n- '
                        response+='\n- '.join(cogs._wiki[entry])
                    else:
                        response+=':** '+cogs._wiki[entry]
            else:
                response+=':** '+cogs._resp['define']['404']

            await ctx.send(response)

# Modes:
# 1: Add (default)
# 0: Add & Modify
# -1: Delete
    @commands.command(**cogs._cmd['edit'])
    async def edit(self, ctx: commands.Context, entry: str, mode:
        Optional[int]=1, *value: str) -> None:
        if cogs._global['playing']=='Debug':
            await ctx.send(cogs._resp['play']['Debug'])
        role_lorekeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild[ctx.guild.id]['lorekeep'])
        if role_lorekeep not in ctx.author.roles:
            await ctx.send(cogs._resp['edit']['403'])
            return

        entry=entry.lower()

        if mode==-1:
            if not cogs._wiki.get(entry):
                await ctx.send(cogs._resp['edit']['404'])
                return

            del cogs._wiki[entry]
            await ctx.send(cogs._resp['edit']['delete'].format(entry))
            # If not returned, export will commence
        else:
            if not len(value):
                await ctx.send(cogs._resp['edit']['empty_entry'])
                return

            if cogs._wiki.get(entry) and mode==1:
                await ctx.send(cogs._resp['edit']['entry_exists'])
                return

            cogs._wiki[entry]=' '.join(value)
            await ctx.send(cogs._resp['edit']['add_mod'].format(entry))
            # If not returned, export will commence
        with open('data/wiki.json', 'w+', encoding='utf-8'
        ) as json_wiki:
            dump(cogs._wiki, json_wiki, sort_keys=True, indent=4)

    @commands.command(**cogs._cmd['mute'])
    async def mute(self, ctx: commands.Context, member: discord.Member,
        hours: str, *reason: str) -> None:
        if cogs._global['playing']=='Debug':
            await ctx.send(cogs._resp['play']['Debug'])
        if member==self.bot.user or (
            not ctx.author.guild_permissions.manage_roles):
            await ctx.send(cogs._resp['mute']['403'])
            return

        hours_float: float=eval(hours, {'__builtins__': None}, None)
        if hours_float<0:
            await ctx.send(cogs._resp['mute']['negative_duration'])
            return

        role_mute: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild[ctx.guild.id]['mute'])
        reason_full: str=' '.join(reason)
        if reason_full=='':
            reason_full='no reason'
        
        response: str=cogs._resp['mute']['mute'].format(member.display_name,
            hours_float, reason_full)
        if member==ctx.author:
            response+=' '+cogs._resp['mute']['self_mute']
        await ctx.send(response)
        await member.add_roles(role_mute, reason=reason_full)

        await asyncio.sleep(hours_float*3600.0)
        response=cogs._resp['mute']['unmute'].format(member.mention,
            hours_float, reason_full)
        if member==ctx.author:
            response+=' '+cogs._resp['mute']['self_mute']
        await ctx.send(response)
        await member.remove_roles(role_mute, reason='Not '+reason_full)

    @commands.command(**cogs._cmd['play'])
    async def play(self, ctx: commands.Context, *game: str) -> None:
        role_botkeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild[ctx.guild.id]['botkeep'])
        if role_botkeep not in ctx.author.roles:
            await ctx.send(cogs._resp['play']['403'])
            return

        game_full: str=' '.join(game)

        if game_full=='':
            await ctx.send(cogs._resp['play']['404'])
            return
        elif game_full in ('Debug', 'debug'):
            await self.bot.change_presence(activity=discord.Game('Debug'),
                status=discord.Status.dnd)
            cogs._global['playing']='Debug'
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)
        elif game_full in ('Nothing, nothing'):
            await self.bot.change_presence(activity=None,
                status=discord.Status.online)
            # Export status for use next launch
            prev_game=cogs._global.pop('playing')
            await ctx.send(cogs._resp['play']['nothing'].format(prev_game))
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)
        else:
            if cogs._resp['play'].get(game_full):
                await ctx.send(cogs._resp['play'][game_full])
            await self.bot.change_presence(activity=discord.Game(game_full),
                status=discord.Status.online)
            # Export status for use next launch
            cogs._global['playing']=game_full
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)

