# Wiki: General information tools.

import cogs
import discord
from discord.ext import commands
from json import dump
import re
from typing import Iterator, Match, Optional

class Wiki(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot
        self._wiki=cogs.load_cfg('wiki')

    @commands.command(**cogs._cmd['define'])
    async def define(self, ctx: commands.Context, *entries: str) -> None:
        if ctx.guild.get_member(self.bot.user.id).status==discord.Status.dnd:
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

            if self._wiki.get(entry):
                # Array entries
                if type(self._wiki[entry])==list:
                    response+=':**\n- '
                    response+='\n- '.join(self._wiki[entry])
                else:
                    # Redirecting entries
                    while self._wiki[entry][0]=='>':
                        entry=self._wiki[entry][1:]
                        response+='→'+entry
                    
                    if type(self._wiki[entry])==list:
                        response+=':**\n- '
                        response+='\n- '.join(self._wiki[entry])
                    else:
                        response+=':** '+self._wiki[entry]
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
        if ctx.guild.get_member(self.bot.user.id).status==discord.Status.dnd:
            await ctx.send(cogs._resp['play']['Debug'])
        role_lorekeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild[ctx.guild.id]['lorekeep'])
        if role_lorekeep not in ctx.author.roles:
            await ctx.send(cogs._resp['edit']['403'])
            return

        entry=entry.lower()

        if mode==-1:
            if not self._wiki.get(entry):
                await ctx.send(cogs._resp['edit']['404'])
                return

            del self._wiki[entry]
            await ctx.send(cogs._resp['edit']['delete'].format(entry))
            # If not returned, export will commence
        else:
            if not len(value):
                await ctx.send(cogs._resp['edit']['empty_entry'])
                return

            if self._wiki.get(entry) and mode==1:
                await ctx.send(cogs._resp['edit']['entry_exists'])
                return

            self._wiki[entry]=' '.join(value)
            await ctx.send(cogs._resp['edit']['add_mod'].format(entry))
            # If not returned, export will commence
        with open('data/wiki.json', 'w+', encoding='utf-8'
        ) as json_wiki:
            dump(self._wiki, json_wiki, sort_keys=True, indent=4)
