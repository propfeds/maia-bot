# Enquiries: Moderation tools.

import asyncio
import cogs
import discord
from discord.ext import commands

class Enquiries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    @commands.command(**cogs._cmd['mute'])
    async def mute(self, ctx: commands.Context, member: discord.Member,
        hours: str, *reason: str) -> None:
        if ctx.guild.get_member(self.bot.user.id).status==discord.Status.dnd:
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
