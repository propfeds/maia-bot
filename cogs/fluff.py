from cogs import responses, guild_emoji
from discord import File
from discord.ext import commands
from utils.grammar import get_random_vowel

class Fluff(commands.Cog, name='Fluff'):
    def __init__(self, bot):
        self.bot=bot

    def format_emoji(self, guild, name):
        return '<:{0}:{1}>'.format(name, guild_emoji[guild.id][name])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author==self.bot.user:
            return

        message_lowcase=message.content.lower()

        if 'wotcher' in message_lowcase:
            await message.add_reaction(self.format_emoji(message.guild, 'wotcher'))

        if 'rougelike' in message_lowcase:
            await message.channel.send(responses['rougelike'].format(get_random_vowel(), get_random_vowel(), get_random_vowel()))

        if 'reanimat' in message_lowcase:
            await message.channel.send(file=File('data/necrobutt.gif'))