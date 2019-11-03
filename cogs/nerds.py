from cogs import responses, randorg_client, die_regex_pattern
import discord
from discord.ext import commands
# pylint: disable=unused-wildcard-import
from math import *
# pylint: enable=unused-wildcard-import
from random import randint, choice
from rdoclient_py3 import RandomOrgSendTimeoutError, RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError
import re
from utils.conversions import f_c, c_f, inch_cm, cm_inch

class Nerds(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    def format_dice(self, match):
        return (int(match.group(1)) if (match.group(1) is not None) else 1, int(match.group(2)), int(match.group(3)) if (match.group(3) is not None) else 0)

    @commands.command(aliases=responses['calc']['aliases'], description=responses['calc']['desc'], help=responses['calc']['help'], brief=responses['calc']['brief'])
    async def calc(self, context, *exp):
        exp_full=''.join(exp)
        await context.send(choice(responses['calc']['result']).format(eval(str(exp_full))))

    @commands.command(description=responses['roll']['desc'], help=responses['roll']['help'], brief=responses['roll']['brief'])
    async def roll(self, context, die, *reason):
        die_match=re.match(die_regex_pattern, die)
        if die_match is None:
            await context.send(responses['roll']['not_die'].format(context.author.display_name))
            return

        repeats=1
        response='{0} `{1}` {2} {3}'.format(responses['roll']['rolling'], die, responses['roll']['for'], context.author.display_name)
        for i, word in enumerate(reason):
            response+=' '
            if not i:
                if word.isdigit():
                    repeats=int(word)
                    response+='{0} {1}'.format(word, responses['roll']['times'])
                    if len(reason)>1:
                        response+=' {0}'.format(responses['roll']['for'])
                else:
                    response+='{0} {1}'.format(responses['roll']['once_for'], word)
            else:
                response+=word
        response+=':'

        dice, sides, mod=self.format_dice(die_match)

        results_dice=[]
        try:
            results_dice.extend(randorg_client.generate_integers(dice*repeats, 1, sides))
        except RandomOrgSendTimeoutError:
            response+='\n{0}'.format(responses['roll']['randorg_timeout'])
        except (RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError):
            response+='\n{0}'.format(responses['roll']['randorg_juice'])
            for _ in range(dice*repeats):
                results_dice.append(randint(1, sides))

        # Actually displaying dice
        for i in range(repeats):
            roll=results_dice[dice*i:dice*(i+1)]
            result_sum=sum(roll, mod)
            response+='\n{0}'.format(responses['roll']['result'].format(str(roll), ('+{0}'.format(mod) if (mod>0) else str(mod)) if (mod!=0) else '', '→{0}'.format(result_sum) if (dice>1 or mod!=0) else ''))

        await context.send(response)