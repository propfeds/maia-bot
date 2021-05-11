# Fluff: Definitely slows the whole bot down,
# since it scans every single message and convert it into lowercase.
# For nothing but memes.

import asyncio
import cogs
import discord
from discord.ext import commands
from random import choice, randint

class Fluff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author==self.bot.user:
            return

        message_lowcase: str=message.content.casefold()
    
        if 'wotcher' in message_lowcase:
            # Wotcher falls back to Cult of the Propaned (hardcoded)
            await message.add_reaction(cogs.get_emoji(message.guild,
                'wotcher', 631772789988392960))

        if 'rougelike' in message_lowcase:
            await message.channel.send(
                cogs._resp['fluff']['rl_base'].format(
                    choice(cogs._resp['fluff']['rouge']).format(
                        choice(cogs._resp['fluff']['vowels']),
                        choice(cogs._resp['fluff']['vowels']),
                        choice(cogs._resp['fluff']['vowels'])
                    ),
                    choice(cogs._resp['fluff']['like']).format(
                        choice(cogs._resp['fluff']['vowels']),
                        choice(cogs._resp['fluff']['vowels'])
                    )
                )
            )

        if 'reanimate' in message_lowcase:
            await message.add_reaction('🤘')
            await asyncio.sleep(randint(14, 21))
            await message.channel.send(file=discord.File(
                'data/images/necrobutt.gif'))

        if 'heh' in message_lowcase or 'hah' in message_lowcase:
            await asyncio.sleep(1)
            if randint(0, 99)<1:
                await message.channel.send(file=discord.File(
                    'data/images/heh.gif'))

        if 'that\'s what he said' in message_lowcase:
            await message.channel.send(file=discord.File(
                'data/images/gachibass.gif'))

    @commands.command(cogs._cmd['scream'])
    async def scream(self, ctx: commands.Context) -> None:
        if cogs._debug_state:
            await ctx.send(cogs._resp['play']['debug_on'])
        await ctx.send(choice(cogs._resp['fluff']['screams']))
