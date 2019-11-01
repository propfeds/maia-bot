from cogs import responses, randorg_client
import discord
from discord.ext import commands
# pylint: disable=unused-wildcard-import
from math import *
# pylint: enable=unused-wildcard-import
from random import randint, choice
from rdoclient_py3 import RandomOrgSendTimeoutError, RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError
from utils.conversions import f_c, c_f, inch_cm, cm_inch

class Nerds(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=responses['calc']['aliases'], description=responses['calc']['desc'], help=responses['calc']['help'], brief=responses['calc']['brief'])
    async def calc(self, context, *exp):
        exp_full=''.join(exp)
        await context.send(choice(responses['calc']['result']).format(eval(str(exp_full))))

    @commands.command(description=responses['roll']['desc'], help=responses['roll']['help'], brief=responses['roll']['brief'])
    async def roll(self, context, die, *reason):
        nof_repeats=1
        response='{0} `{1}` for {2}'.format(responses['roll']['rolling'], die, context.author.display_name)
        for i, word in enumerate(reason):
            response+=' '
            if not i:
                if word.isdigit():
                    nof_repeats=int(word)
                    response+='{0} {1}'.format(word, responses['roll']['times'])
                    if len(reason)>1:
                        response+=' {0}'.format(responses['roll']['for'])
                else:
                    response+='{0} {1}'.format(responses['roll']['once_for'], word)
            else:
                response+=word
        response+=':'

        # Replacing 'd' and '+' with spaces
        die_list=die.translate({100:32, 43:32}).split()
        die_list.append('0')
        dice, sides, mod=int(die_list[0]), int(die_list[1]), int(die_list[2])

        results_dice=[]
        try:
            results_dice.extend(randorg_client.generate_integers(dice*nof_repeats, 1, sides))
        except RandomOrgSendTimeoutError:
            response+='\n{0}'.format(responses['roll']['randorg_timeout'])
        except (RandomOrgInsufficientRequestsError, RandomOrgInsufficientBitsError):
            response+='\n{0}'.format(responses['roll']['randorg_juice'])
            for _ in range(dice*nof_repeats):
                results_dice.append(randint(1, sides))

        # Actually displaying dice
        for i in range(nof_repeats):
            roll=results_dice[dice*i:dice*(i+1)]
            response+='\n`{0}`→{1}'.format(str(roll), sum(roll)+mod)

        await context.send(response)