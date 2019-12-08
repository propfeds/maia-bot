import asyncio
from cogs import responses, commands_wiki, get_role, bard_rare_chance, gungeoneer_role_name
import discord
from discord.ext import commands
from random import randint
from utils.grammar import get_possessive

class Queries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot=bot

    @commands.command(
        aliases=responses['bard']['cfg']['aliases'],
        brief=responses['bard']['cfg']['brief'],
        description=responses['bard']['cfg']['desc'],
        help=responses['bard']['cfg']['help'],
        hidden=responses['bard']['cfg']['hidden']
    )
    async def bard(self, context: commands.Context) -> None:
        if get_role(context.guild, 'Bard') in context.author.roles:
            await context.author.remove_roles(get_role(context.guild, 'Bard'), reason=responses['bard']['unbard_reason'])
            await context.send(responses['bard']['unbard'].format(context.author.display_name))
        else:
            await context.author.add_roles(get_role(context.guild, 'Bard'), reason=responses['bard']['bard_reason'])
            roll_rare=randint(0, 99)
            if roll_rare<bard_rare_chance:
                await context.send(responses['bard']['bard_rare'].format(context.author.display_name, get_possessive(context.author.display_name)))
            else:
                await context.send(responses['bard']['bard'].format(context.author.display_name))

    @commands.command(
        aliases=responses['mute']['cfg']['aliases'],
        brief=responses['mute']['cfg']['brief'],
        description=responses['mute']['cfg']['desc'],
        help=responses['mute']['cfg']['help'],
        hidden=responses['mute']['cfg']['hidden']
    )
    async def mute(self, context: commands.Context, member: discord.Member, hours: float, *reason: str) -> None:
        if member==self.bot.user or not context.author.guild_permissions.manage_roles:
            await context.send(responses['mute']['fool'])
            return

        hours_int=eval(str(hours))
        if hours_int<0:
            await context.send(responses['mute']['negative_duration'])
            return

        reason_full=' '.join(reason)
        response=responses['mute']['mute'].format(member.display_name, hours_int, reason_full)
        if member==context.author:
            response+=' {0}'.format(responses['mute']['fool'])
        await context.send(response)
        await member.add_roles(get_role(context.guild, gungeoneer_role_name), reason=reason_full)

        await asyncio.sleep(hours_int*3600.0)
        response=responses['mute']['unmute'].format(member.mention, hours_int, reason_full)
        if member==context.author:
            response+=' {0}'.format(responses['mute']['fool'])
        await context.send(response)
        await member.remove_roles(get_role(context.guild, gungeoneer_role_name), reason='Not '+reason_full)

    @commands.command(
        aliases=responses['sourcerer']['cfg']['aliases'],
        brief=responses['sourcerer']['cfg']['brief'],
        description=responses['sourcerer']['cfg']['desc'],
        help=responses['sourcerer']['cfg']['help'],
        hidden=responses['sourcerer']['cfg']['hidden']
    )
    async def sourcerer(self, context: commands.Context) -> None:
        if get_role(context.guild, 'Sourcerer') in context.author.roles:
            await context.author.remove_roles(get_role(context.guild, 'Sourcerer'), reason=responses['sourcerer']['unsource_reason'])
            await context.send(responses['sourcerer']['unsource'].format(context.author.display_name))
        else:
            await context.author.add_roles(get_role(context.guild, 'Sourcerer'), reason=responses['sourcerer']['source_reason'])
            await context.send(responses['sourcerer']['source'].format(context.author.display_name))

    @commands.command(
        aliases=responses['wiki']['cfg']['aliases'],
        brief=responses['wiki']['cfg']['brief'],
        description=responses['wiki']['cfg']['desc'],
        help=responses['wiki']['cfg']['help'],
        hidden=responses['wiki']['cfg']['hidden']
    )
    async def wiki(self, context: commands.Context, *entry: str) -> None:
        entry_full=' '.join(entry).lower()
        response='**{0}'.format(entry_full)

        if commands_wiki.get(entry_full):
            # Array entries
            if type(commands_wiki[entry_full])==list:
                response+=':**\n- '
                response+='\n- '.join(commands_wiki[entry_full])
            else:
                # Redirecting entries
                while commands_wiki[entry_full][0]=='>':
                    entry_full=commands_wiki[entry_full][1:]
                    response+='→{0}'.format(entry_full)
                
                if type(commands_wiki[entry_full])==list:
                    response+=':**\n- '
                    response+='\n- '.join(commands_wiki[entry_full])
                else:
                    response+=':** {0}'.format(commands_wiki[entry_full])
        else:
            response+=':** {0}'.format(responses['wiki']['entry_not_exist'])

        await context.send(response)
