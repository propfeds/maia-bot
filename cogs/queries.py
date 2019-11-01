from cogs import responses, commands_wiki, get_role, bard_rare_chance
import discord
from discord.ext import commands
from random import randint
from utils.grammar import get_possessive

class Queries(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(description=responses['bard']['desc'], help=responses['bard']['help'], brief=responses['bard']['brief'])
    async def bard(self, context):
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

    @commands.command(aliases=responses['wiki']['aliases'], description=responses['wiki']['desc'], help=responses['wiki']['help'], brief=responses['wiki']['brief'])
    async def wiki(self, context, *entry):
        entry_full=' '.join(entry).lower()

        response='**{0}'.format(entry_full)
        if commands_wiki.get(entry_full):
            # Redirecting entries
            while commands_wiki.get(entry_full)[0]=='>':
                entry_full=commands_wiki.get(entry_full)[1:]
                response+='→{0}'.format(entry_full)

            response+=':** {0}'.format(commands_wiki.get(entry_full))
        else:
            response+=':** {0}'.format(responses['wiki']['entry_not_exist'])

        await context.send(response)