# Nerds: Contains mathematical tools.

import cogs
import discord
from discord.ext import commands
from random import randint, choice
from rdoclient_py3 import (RandomOrgSendTimeoutError,
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

    @commands.command(
        aliases=cogs.cfg['calc']['aliases'],
        brief=cogs.cfg['calc']['brief'],
        description=cogs.cfg['calc']['desc'],
        help=cogs.cfg['calc']['help'],
        hidden=cogs.cfg['calc']['hidden']
    )
    async def calc(self, ctx: commands.Context, *exp: str) -> None:
        if cogs._debug_state:
            role_botkeep: discord.Role=cogs.get_role(ctx.guild,
                cogs.guild_cfg[ctx.guild.id]['botkeep'])
            if role_botkeep not in ctx.author.roles:
                await ctx.send(cogs.resp['calc']['debug_locked'])
                return
            await ctx.send(choice(cogs.resp['calc']['result']).format(eval(
                ''.join(exp))))
        else:
            await ctx.send(choice(cogs.resp['calc']['result']).format(eval(
                ''.join(exp), {"__builtins__": None}, cogs.math_func_dict)))

    @commands.command(
        aliases=cogs.cfg['roll']['aliases'],
        brief=cogs.cfg['roll']['brief'],
        description=cogs.cfg['roll']['desc'],
        help=cogs.cfg['roll']['help'],
        hidden=cogs.cfg['roll']['hidden']
    )
    async def roll(self, ctx: commands.Context, die: str, repeats: Optional
    [int]=1, *reason: str) -> None:
        if cogs._debug_state:
            await ctx.send(cogs.resp['play']['debug_on'])
        die_match: Match=re.match(cogs.die_regex, die)
        if die_match is None:
            await ctx.send(cogs.resp['roll']['not_die'].format(
                ctx.author.display_name))
            return
        else:
            dice: int; sides: int; mod: int
            dice, sides, mod=self.die_tuple(die_match)
            if not dice*repeats:
                await ctx.send(cogs.resp['roll']['no_dice'])
                return
            elif dice*repeats<0:
                await ctx.send(cogs.resp['roll']['negative_dice'])
                return
            elif sides<=1:
                await ctx.send(cogs.resp['roll']['not_die'].format(
                    ctx.author.display_name))
                return

        response: str=cogs.resp['roll']['rolling_for'].format(die,
            ctx.author.display_name)
        response+=' '
        if repeats>1:
            response+=cogs.resp['roll']['times'].format(repeats)
        else:
            response+=cogs.resp['roll']['once']

        if len(reason):
            response+=' ('+' '.join(reason)+')'

        response+=':'

        results: List[int]=[]

        if version_info.major==3 and version_info.minor==8:
            response+='\n'+cogs.resp['roll']['py_38_time']
            for _ in range(dice*repeats):
                results.append(randint(1, sides))
        else:
            try:
                results.extend(cogs.randorg_client.generate_integers(
                    dice*repeats, 1, sides))
            except RandomOrgSendTimeoutError:
                response+='\n'+cogs.resp['roll']['randorg_timeout']
            except (RandomOrgInsufficientRequestsError,
            RandomOrgInsufficientBitsError):
                response+='\n'+cogs.resp['roll']['randorg_juice']
                for _ in range(dice*repeats):
                    results.append(randint(1, sides))

        # Actually displaying dice
        for i in range(repeats):
            roll: List[int]=results[dice*i:dice*(i+1)]
            # Oh the format monstrosities
            response+='\n`{0}{1}`{2}'.format(
                str(roll),
                ('+'+str(mod) if mod>0 else str(mod)) if mod!=0 else '',
                '→'+str(sum(roll, mod)) if (dice>1 or mod!=0) else ''
            )

        await ctx.send(response)
