# Calc: Contains mathematical tools.

import cogs
import discord
from discord.ext import commands
import math
from random import choice
from typing import Callable, Dict

class Calculator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot
        self._math: Dict[str, Callable]={
            'ceil': math.ceil, 'comb': math.comb, 'copysign': math.copysign,
            'abs': math.fabs, 'factorial': math.factorial, 'floor': math.floor,
            'fmod': math.fmod, 'frexp': math.frexp, 'fsum': math.fsum,
            'gcd': math.gcd, 'isclose': math.isclose,
            'isfinite': math.isfinite, 'isinf': math.isinf,
            'isnan': math.isnan, 'isqrt': math.isqrt, 'ldexp': math.ldexp,
            'modf': math.modf, 'perm': math.perm, 'prod': math.prod,
            'remainder': math.remainder, 'trunc': math.trunc, 'exp': math.exp,
            'expm1': math.expm1, 'log': math.log, 'log1p': math.log1p,
            'log2': math.log2, 'log10': math.log10, 'pow': math.pow,
            'sqrt': math.sqrt, 'acos': math.acos, 'asin': math.asin,
            'atan': math.atan, 'atan2': math.atan2, 'cos': math.cos,
            'dist': math.dist, 'hypot': math.hypot, 'sin': math.sin,
            'tan': math.tan, 'degrees': math.degrees, 'radians': math.radians,
            'acosh': math.acosh, 'asinh': math.asinh, 'atanh': math.atanh,
            'cosh': math.cosh, 'sinh': math.sinh, 'tanh': math.tanh,
            'erf': math.erf, 'erfc': math.erfc, 'gamma': math.gamma,
            'lgamma': math.lgamma, 'pi': math.pi, 'e': math.e, 'tau': math.tau,
            'inf': math.inf, 'nan': math.nan
        }
    
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
                ''.join(exp), {'__builtins__': None}, self._math)))
