from cogs import gather
from cogs.fluff import Fluff
from cogs.nerds import Nerds
from cogs.queries import Queries
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot=commands.Bot(command_prefix=['!', 'Maia, ', 'maia, ', 'MAIA, '])

@bot.event
async def on_ready():
    # Steal all your data
    guild_id_prop=int(os.getenv('DISCORD_GUILD_ID_PROP'))
    for guild in bot.guilds:
        if guild.id==guild_id_prop:
            gather(guild, True)
        else:
            gather(guild)

    print('Maia the {0}, rolling out in the age of {1}!'.format(bot.user.name, discord.__version__))

bot.add_cog(Queries(bot))
bot.add_cog(Fluff(bot))
bot.add_cog(Nerds(bot))
bot.run(os.getenv('DISCORD_TOKEN'))