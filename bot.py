import cogs
from cogs.core import Core
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

bot: commands.Bot=commands.Bot(command_prefix=cogs._global['prefixes'])

bot.add_cog(Core(bot))
core=bot.get_cog('Core')
for cog in cogs._global['autoruns']:
    core.construct_cog(cog)

load_dotenv()
bot.run(getenv('DISCORD_TOKEN'))
