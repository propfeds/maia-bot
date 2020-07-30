# Fluff: Definitely slows the whole bot down,
# since it scans every single message and convert it into lowercase.

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

        if 'reanimate' in message_lowcase:
            await message.add_reaction('🤘')
            await asyncio.sleep(randint(4, 11))
            await message.channel.send(file=discord.File('data/necrobutt.gif'))

        if 'heh' in message_lowcase:
            await asyncio.sleep(1)
            if randint(0, 99)<3:
                await message.channel.send(file=discord.File('data/heh.gif'))

        if 'that\'s what he said' in message_lowcase:
            await message.channel.send(file=discord.File('data/gachibass.gif'))

    @commands.command(
        aliases=cogs.cfg['scream']['aliases'],
        brief=cogs.cfg['scream']['brief'],
        description=cogs.cfg['scream']['desc'],
        help=cogs.cfg['scream']['help'],
        hidden=cogs.cfg['scream']['hidden']
    )
    async def scream(self, ctx: commands.Context) -> None:
        if cogs._debug_state:
            await ctx.send(cogs.resp['play']['debug_on'])
        await ctx.send(choice(cogs.resp['fluff']['screams']))
