import cogs
import discord
from discord.ext import commands
from random import choice
from utils.grammar import get_random_vowel

class Fluff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    def format_emoji(self, guild: discord.Guild, name: str) -> str:
        return '<:{0}:{1}>'.format(name, cogs.emoji_id[guild.id][name])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author==self.bot.user:
            return

        message_lowcase: str=message.content.lower()

        if 'wotcher' in message_lowcase:
            await message.add_reaction(self.format_emoji(message.guild, 'wotcher'))

        if 'rougelike' in message_lowcase:
            await message.channel.send(cogs.resp['rougelike'].format(get_random_vowel(), get_random_vowel(), get_random_vowel()))

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
        await context.send(choice(cogs.resp['scream']['screams']))
