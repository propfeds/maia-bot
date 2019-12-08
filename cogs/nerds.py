import cogs
from discord.ext import commands
# pylint: disable=unused-wildcard-import
from math import *
from random import randint, choice
from rdoclient_py3 import RandomOrgSendTimeoutError, RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError
import re
from typing import List, Match, Optional, Tuple
from utils.conversions import *
# pylint: enable=unused-wildcard-import

class Nerds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

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
        await context.send(choice(cogs.resp['calc']['result']).format(eval(''.join(exp))))

    @commands.command(
        aliases=cogs.cfg['roll']['aliases'],
        brief=cogs.cfg['roll']['brief'],
        description=cogs.cfg['roll']['desc'],
        help=cogs.cfg['roll']['help'],
        hidden=cogs.cfg['roll']['hidden']
    )
    async def roll(self, context: commands.Context, die: str, repeats: Optional[int]=1, *reason: str) -> None:
        die_match: Match=re.match(cogs.die_regex, die)
        if die_match is None:
            await context.send(cogs.resp['roll']['not_die'].format(context.author.display_name))
            return
        else:
            dice: int; sides: int; mod: int
            dice, sides, mod=self.format_dice(die_match)
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
