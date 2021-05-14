# Nerds: Contains mathematical tools.

import cogs
import discord
from discord.ext import commands
from random import choice
from rdoclient import (RandomOrgSendTimeoutError,
RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError)
import re
from sys import version_info
from typing import List, Match, Optional, Tuple

class Nerds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    def die_tuple(self, match: Match) -> Tuple[int, int, int]:
        return (
            int(match.group(1)) if (match.group(1) is not None) else 1,
            int(match.group(2)),
            int(match.group(3)) if (match.group(3) is not None) else 0
        )

    @commands.command(**cogs._cmd['calc'])
    async def calc(self, ctx: commands.Context, *exp: str) -> None:
        if cogs._global['playing']=='Debug':
            role_botkeep: discord.Role=cogs.get_role(ctx.guild,
                cogs._guild[ctx.guild.id]['botkeep'])
            if role_botkeep not in ctx.author.roles:
                await ctx.send(cogs._resp['calc']['debug_locked'])
                return
            await ctx.send(choice(cogs._resp['calc']['result']).format(eval(
                ''.join(exp))))
        else:
            await ctx.send(choice(cogs._resp['calc']['result']).format(eval(
                ''.join(exp), {'__builtins__': None}, cogs._math_func_dict)))

    @commands.command(**cogs._cmd['roll'])
    async def roll(self, ctx: commands.Context, die: str, repeats: Optional
    [int]=1, *reason: str) -> None:
        if cogs._global['playing']=='Debug':
            await ctx.send(cogs._resp['play']['Debug'])
        die_match: Match=re.match(r'(\d+)?[dD](\d+)([\+\-]\d+)?', die)
        if die_match is None:
            await ctx.send(cogs._resp['roll']['not_die'].format(
                ctx.author.display_name))
            return
        else:
            dice: int; sides: int; mod: int
            dice, sides, mod=self.die_tuple(die_match)
            if not dice*repeats:
                await ctx.send(cogs._resp['roll']['no_dice'])
                return
            elif dice*repeats<0:
                await ctx.send(cogs._resp['roll']['negative_dice'])
                return
            elif sides<=1:
                await ctx.send(cogs._resp['roll']['not_die'].format(
                    ctx.author.display_name))
                return

        response: str=cogs._resp['roll']['rolling_for'].format(die,
            ctx.author.display_name)
        response+=' '
        if repeats>1:
            response+=cogs._resp['roll']['times'].format(repeats)
        else:
            response+=cogs._resp['roll']['once']

        if len(reason):
            response+=' ('+' '.join(reason)+')'

        response+=':\n'

        results, err_resp=cogs.roll_array(dice*repeats, sides)
        response+=err_resp
        
        # Actually displaying dice
        for i in range(repeats):
            roll: List[int]=results[dice*i:dice*(i+1)]
            # Oh the format monstrosities
            response+='`{0}{1}`{2}\n'.format(
                str(roll),
                ('+'+str(mod) if mod>0 else str(mod)) if mod!=0 else '',
                '→'+str(sum(roll, mod)) if (dice>1 or mod!=0) else ''
            )

        await ctx.send(response)
