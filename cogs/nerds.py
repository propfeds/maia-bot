import cogs
import discord
from discord.ext import commands
import math
from random import randint, choice
from rdoclient_py3 import RandomOrgSendTimeoutError, RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError
import re
from sys import version_info
from typing import List, Match, Optional, Tuple

class Nerds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot
        self.func_dict={
            'ceil': math.ceil,
            'comb': math.comb,
            'copysign': math.copysign,
            'abs': math.fabs,
            'factorial': math.factorial,
            'floor': math.floor,
            'fmod': math.fmod,
            'frexp': math.frexp,
            'fsum': math.fsum,
            'gcd': math.gcd,
            'isclose': math.isclose,
            'isfinite': math.isfinite,
            'isinf': math.isinf,
            'isnan': math.isnan,
            'isqrt': math.isqrt,
            'ldexp': math.ldexp,
            'modf': math.modf,
            'perm': math.perm,
            'prod': math.prod,
            'remainder': math.remainder,
            'trunc': math.trunc,
            'exp': math.exp,
            'expm1': math.expm1,
            'log': math.log,
            'log1p': math.log1p,
            'log2': math.log2,
            'log10': math.log10,
            'pow': math.pow,
            'sqrt': math.sqrt,
            'acos': math.acos,
            'asin': math.asin,
            'atan': math.atan,
            'atan2': math.atan2,
            'cos': math.cos,
            'dist': math.dist,
            'hypot': math.hypot,
            'sin': math.sin,
            'tan': math.tan,
            'degrees': math.degrees,
            'radians': math.radians,
            'acosh': math.acosh,
            'asinh': math.asinh,
            'atanh': math.atanh,
            'cosh': math.cosh,
            'sinh': math.sinh,
            'tanh': math.tanh,
            'erf': math.erf,
            'erfc': math.erfc,
            'gamma': math.gamma,
            'lgamma': math.lgamma,
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'inf': math.inf,
            'nan': math.nan
        }

    def format_dice(self, match: Match) -> Tuple[int, int, int]:
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
    async def calc(self, context: commands.Context, *exp: str) -> None:
        if cogs.debug_state:
            role_botkeep=cogs.get_role_from_id(context.guild, cogs.guild_cfg[context.guild.id]['roles']['botkeep'])
            if role_botkeep not in context.author.roles:
                await context.send(cogs.resp['calc']['debug_locked'])
                return
            await context.send(choice(cogs.resp['calc']['result']).format(eval(''.join(exp))))
        else:
            await context.send(choice(cogs.resp['calc']['result']).format(eval(''.join(exp), {"__builtins__": None}, self.func_dict)))

    @commands.command(
        aliases=cogs.cfg['debug']['aliases'],
        brief=cogs.cfg['debug']['brief'],
        description=cogs.cfg['debug']['desc'],
        help=cogs.cfg['debug']['help'],
        hidden=cogs.cfg['debug']['hidden']
    )
    async def debug(self, context: commands.Context) -> None:
        role_botkeep=cogs.get_role_from_id(context.guild, cogs.guild_cfg[context.guild.id]['roles']['botkeep'])
        if role_botkeep not in context.author.roles:
            await context.send(cogs.resp['debug']['403'])
            return

        # Now really toggles
        cogs.debug_state=not cogs.debug_state
        if cogs.debug_state:
            await context.send(cogs.resp['debug']['on'])
            await self.bot.change_presence(activity=discord.Game('Debug'), status=discord.Status.dnd)
        else:
            await context.send(cogs.resp['debug']['off'])
            await self.bot.change_presence(activity=None, status=discord.Status.online)

    @commands.command(
        aliases=cogs.cfg['roll']['aliases'],
        brief=cogs.cfg['roll']['brief'],
        description=cogs.cfg['roll']['desc'],
        help=cogs.cfg['roll']['help'],
        hidden=cogs.cfg['roll']['hidden']
    )
    async def roll(self, context: commands.Context, die: str, repeats: Optional[int]=1, *reason: str) -> None:
        if cogs.debug_state:
            await context.send(cogs.resp['debug']['on'])
        die_match: Match=re.match(cogs.die_regex, die)
        if die_match is None:
            await context.send(cogs.resp['roll']['not_die'].format(context.author.display_name))
            return
        else:
            dice: int; sides: int; mod: int
            dice, sides, mod=self.format_dice(die_match)
            if not dice*repeats:
                await context.send(cogs.resp['roll']['no_dice'])
                return
            elif dice*repeats<0:
                await context.send(cogs.resp['roll']['negative_dice'])
                return
            elif sides<=1:
                await context.send(cogs.resp['roll']['not_die'].format(context.author.display_name))
                return

        response: str=cogs.resp['roll']['rolling_for'].format(die, context.author.display_name)
        response+=' '
        if repeats>1:
            response+=cogs.resp['roll']['times'].format(repeats)
        else:
            response+=cogs.resp['roll']['once']

        if len(reason):
            response+=' ({0})'.format(' '.join(reason))

        response+=':'

        results: List[int]=[]

        if version_info.major==3 and version_info.minor==8:
            response+='\n{0}'.format(cogs.resp['roll']['py_38_time'])
            for _ in range(dice*repeats):
                results.append(randint(1, sides))
        else:
            try:
                results.extend(cogs.randorg_client.generate_integers(dice*repeats, 1, sides))
            except RandomOrgSendTimeoutError:
                response+='\n{0}'.format(cogs.resp['roll']['randorg_timeout'])
            except (RandomOrgInsufficientRequestsError,
            RandomOrgInsufficientBitsError):
                response+='\n{0}'.format(cogs.resp['roll']['randorg_juice'])
                for _ in range(dice*repeats):
                    results.append(randint(1, sides))

        # Actually displaying dice
        for i in range(repeats):
            roll: List[int]=results[dice*i:dice*(i+1)]
            # Oh the format monstrosities
            response+='\n`{0}{1}`{2}'.format(
                str(roll),
                ('+{0}'.format(mod) if mod>0 else str(mod)) if mod!=0 else '',
                '→{0}'.format(sum(roll, mod)) if (dice>1 or mod!=0) else ''
            )

        await context.send(response)
