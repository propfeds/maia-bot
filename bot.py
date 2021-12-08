import asyncio
from asyncio.events import AbstractEventLoop
import cogs
from cogs.core import Core
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

async def autorun(bot: commands.Bot, cogs: list) -> None:
    core: commands.Cog=bot.get_cog('Core')
    tasks=[core.construct_cog(cog, False) for cog in cogs]
    await asyncio.wait(tasks)

bot: commands.Bot=commands.Bot(command_prefix=cogs._global['prefixes'],
    case_insensitive=True)

bot.add_cog(Core(bot))
loop: AbstractEventLoop=asyncio.get_event_loop()
run=loop.run_until_complete(autorun(bot, cogs._global['autoruns']))

load_dotenv()
bot.run(getenv('DISCORD_TOKEN'))
