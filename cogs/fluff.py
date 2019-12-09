import cogs
import discord
from discord.ext import commands
from random import choice

class Fluff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author==self.bot.user:
            return

        message_lowcase: str=message.content.lower()

        if 'wotcher' in message_lowcase:
            await message.add_reaction(cogs.format_emoji(message.guild, 'wotcher'))

        if 'rougelike' in message_lowcase:
            await message.channel.send(
                cogs.resp['fluff']['rl_base'].format(
                    choice(cogs.resp['fluff']['rouge']).format(
                        choice(cogs.resp['fluff']['vowels']),
                        choice(cogs.resp['fluff']['vowels']),
                        choice(cogs.resp['fluff']['vowels'])
                    ),
                    choice(cogs.resp['fluff']['like']).format(
                        choice(cogs.resp['fluff']['vowels']),
                        choice(cogs.resp['fluff']['vowels'])
                    )
                )
            )

        if 'reanimat' in message_lowcase:
            await message.channel.send(file=discord.File('data/necrobutt.gif'))

    @commands.command(
        aliases=cogs.cfg['scream']['aliases'],
        brief=cogs.cfg['scream']['brief'],
        description=cogs.cfg['scream']['desc'],
        help=cogs.cfg['scream']['help'],
        hidden=cogs.cfg['scream']['hidden']
    )
    async def scream(self, context: commands.Context) -> None:
        if cogs.debug_state:
            await context.send(cogs.resp['debug']['on'])
        await context.send(choice(cogs.resp['fluff']['screams']))
