import asyncio
import cogs
import discord
from discord.ext import commands
from json import dump
from random import randint
from typing import Optional
from utils.grammar import get_possessive

class Queries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    @commands.command(
        aliases=cogs.cfg['bard']['aliases'],
        brief=cogs.cfg['bard']['brief'],
        description=cogs.cfg['bard']['desc'],
        help=cogs.cfg['bard']['help'],
        hidden=cogs.cfg['bard']['hidden']
    )
    async def bard(self, context: commands.Context) -> None:
        if cogs.get_role(context.guild, 'Bard') in context.author.roles:
            await context.author.remove_roles(cogs.get_role(context.guild, 'Bard'), reason=cogs.resp['bard']['unbard_reason'])
            await context.send(cogs.resp['bard']['unbard'].format(context.author.display_name))
        else:
            await context.author.add_roles(cogs.get_role(context.guild, 'Bard'), reason=cogs.resp['bard']['bard_reason'])
            roll_rare: int=randint(0, 99)
            if roll_rare<cogs.bard_rare_chance:
                await context.send(cogs.resp['bard']['bard_rare'].format(context.author.display_name, get_possessive(context.author.display_name)))
            else:
                await context.send(cogs.resp['bard']['bard'].format(context.author.display_name))

    @commands.command(
        aliases=cogs.cfg['define']['aliases'],
        brief=cogs.cfg['define']['brief'],
        description=cogs.cfg['define']['desc'],
        help=cogs.cfg['define']['help'],
        hidden=cogs.cfg['define']['hidden']
    )
    async def define(self, context: commands.Context, *entry: str) -> None:
        entry_full: str=' '.join(entry).lower()
        response: str='**{0}'.format(entry_full)

        if cogs.wiki.get(entry_full):
            # Array entries
            if type(cogs.wiki[entry_full])==list:
                response+=':**\n- '
                response+='\n- '.join(cogs.wiki[entry_full])
            else:
                # Redirecting entries
                while cogs.wiki[entry_full][0]=='>':
                    entry_full=cogs.wiki[entry_full][1:]
                    response+='→{0}'.format(entry_full)
                
                if type(cogs.wiki[entry_full])==list:
                    response+=':**\n- '
                    response+='\n- '.join(cogs.wiki[entry_full])
                else:
                    response+=':** {0}'.format(cogs.wiki[entry_full])
        else:
            response+=':** {0}'.format(cogs.resp['define']['404'])

        await context.send(response)

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
    async def modifine(self, context: commands.Context, entry: str, mode: Optional[int]=1, *value: str) -> None:
        if cogs.get_role(context.guild, 'Headmaster') not in context.author.roles:
            await context.send(cogs.resp['modifine']['403'])
            return

        entry=entry.lower()

        if mode==-1:
            if not cogs.wiki.get(entry):
                await context.send(cogs.resp['modifine']['404'])
                return

            del cogs.wiki[entry]
            await context.send(cogs.resp['modifine']['delete'].format(entry))
            # If not returned, export will commence
        else:
            if not len(value):
                await context.send(cogs.resp['modifine']['empty_entry'])
                return

            if cogs.wiki.get(entry) and mode==1:
                await context.send(cogs.resp['modifine']['entry_exists'])
                return

            cogs.wiki[entry]=' '.join(value)
            await context.send(cogs.resp['modifine']['add_mod'].format(entry))
            # If not returned, export will commence
        with open('data/commands/wiki.json', 'w+', encoding='utf-8') as json_wiki:
            dump(cogs.wiki, json_wiki, sort_keys=True, indent=4)

    @commands.command(
        aliases=cogs.cfg['mute']['aliases'],
        brief=cogs.cfg['mute']['brief'],
        description=cogs.cfg['mute']['desc'],
        help=cogs.cfg['mute']['help'],
        hidden=cogs.cfg['mute']['hidden']
    )
    async def mute(self, context: commands.Context, member: discord.Member, hours: str, *reason: str) -> None:
        if member==self.bot.user or not context.author.guild_permissions.manage_roles:
            await context.send(cogs.resp['mute']['403'])
            return

        hours_float: float=eval(hours)
        if hours_float<0:
            await context.send(cogs.resp['mute']['negative_duration'])
            return

        reason_full: str=' '.join(reason)
        response: str=cogs.resp['mute']['mute'].format(member.display_name, hours_float, reason_full)
        if member==context.author:
            response+=' {0}'.format(cogs.resp['mute']['self_mute'])
        await context.send(response)
        await member.add_roles(cogs.get_role(context.guild, cogs.gungeoneer_role_name), reason=reason_full)

        await asyncio.sleep(hours_float*3600.0)
        response=cogs.resp['mute']['unmute'].format(member.mention, hours_float, reason_full)
        if member==context.author:
            response+=' {0}'.format(cogs.resp['mute']['self_mute'])
        await context.send(response)
        await member.remove_roles(cogs.get_role(context.guild, cogs.gungeoneer_role_name), reason='Not '+reason_full)

    @commands.command(
        aliases=cogs.cfg['sourcerer']['aliases'],
        brief=cogs.cfg['sourcerer']['brief'],
        description=cogs.cfg['sourcerer']['desc'],
        help=cogs.cfg['sourcerer']['help'],
        hidden=cogs.cfg['sourcerer']['hidden']
    )
    async def sourcerer(self, context: commands.Context) -> None:
        if cogs.get_role(context.guild, 'Sourcerer') in context.author.roles:
            await context.author.remove_roles(cogs.get_role(context.guild, 'Sourcerer'), reason=cogs.resp['sourcerer']['unsource_reason'])
            await context.send(cogs.resp['sourcerer']['unsource'].format(context.author.display_name))
        else:
            await context.author.add_roles(cogs.get_role(context.guild, 'Sourcerer'), reason=cogs.resp['sourcerer']['source_reason'])
            await context.send(cogs.resp['sourcerer']['source'].format(context.author.display_name))
