from cogs import responses, guild_emoji
import discord
from discord.ext import commands
from random import choice
from utils.grammar import get_random_vowel

class Fluff(commands.Cog, name='Fluff'):
    def __init__(self, bot: commands.Bot):
        self.bot=bot

    def format_emoji(self, guild: discord.Guild, name: str) -> str:
        return '<:{0}:{1}>'.format(name, guild_emoji[guild.id][name])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author==self.bot.user:
            return

        message_lowcase=message.content.lower()

        if 'wotcher' in message_lowcase:
            await message.add_reaction(self.format_emoji(message.guild, 'wotcher'))

        if 'rougelike' in message_lowcase:
            await message.channel.send(responses['rougelike'].format(get_random_vowel(), get_random_vowel(), get_random_vowel()))

        if 'reanimat' in message_lowcase:
            await message.channel.send(file=discord.File('data/necrobutt.gif'))

    @commands.command(
        aliases=responses['scream']['cfg']['aliases'],
        brief=responses['scream']['cfg']['brief'],
        description=responses['scream']['cfg']['desc'],
        help=responses['scream']['cfg']['help'],
        hidden=responses['scream']['cfg']['hidden']
    )
    async def scream(self, context: commands.Context) -> None:
        await context.send(choice(responses['scream']['screams']))