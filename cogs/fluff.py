import discord
from discord.ext import commands
from modules.grammar import get_random_vowel

class Fluff(commands.Cog, name='Fluff'):
    def __init__(self, bot, guild_emoji, responses):
        self.bot=bot
        self.guild_emoji=guild_emoji
        self.responses=responses

    def format_emoji(self, name):
        return '<:{0}:{1}>'.format(name, self.guild_emoji[name])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author==self.bot.user:
            return

        message_lowcase=message.content.lower()

        if 'wotcher' in message_lowcase:
            await message.add_reaction(self.format_emoji('wotcher'))

        if 'rougelike' in message_lowcase:
            await message.channel.send(self.responses['rougelike'].format(get_random_vowel, get_random_vowel, get_random_vowel))