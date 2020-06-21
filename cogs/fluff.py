# Fluff: Definitely slows the whole bot down,
# since it scans every single message and convert it into lowercase.

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

        message_lowcase: str=message.content.lower()

        if message_lowcase=='😱':
            await message.channel.send(choice(cogs.resp['fluff']['screams']))
    
        if 'wotcher' in message_lowcase:
            # Wotcher falls back to Cult of the Propaned (hardcoded)
            await message.add_reaction(cogs.format_emoji(message.guild,
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

        if 'reanimat' in message_lowcase:
            await message.channel.send(file=discord.File('data/necrobutt.gif'))

        if 'jarikeks' in message_lowcase:
            await message.channel.send(file=discord.File('data/heh.gif'))

        if 'that\'s what he said' in message_lowcase:
            await message.channel.send(file=discord.File('data/gachibass.gif'))

        if 'get outta my swamp' in message_lowcase:
            async for m in message.channel.history(limit=13, before=message):
                if randint(0, 99)<10:
                    await m.add_reaction(cogs.format_emoji(message.guild,
                        'OG', 722745447088783422))
                else:
                    await m.add_reaction(cogs.format_emoji(message.guild,
                        'ogre', 560120290072461322))

    @commands.command(
        aliases=cogs.cfg['scream']['aliases'],
        brief=cogs.cfg['scream']['brief'],
        description=cogs.cfg['scream']['desc'],
        help=cogs.cfg['scream']['help'],
        hidden=cogs.cfg['scream']['hidden']
    )
    async def scream(self, context: commands.Context) -> None:
        if cogs._debug_state:
            await context.send(cogs.resp['play']['debug_on'])
        await context.send(choice(cogs.resp['fluff']['screams']))
