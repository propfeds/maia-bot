from cogs import get_cfg
from cogs.fluff import Fluff
from cogs.nerds import Nerds
from cogs.queries import Queries
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot: commands.Bot=commands.Bot(command_prefix=['!', 'Maia, ', 'maia, ',
    'MAIA, ', 'Maia ', 'maia ', 'MAIA '])

@bot.event
async def on_ready() -> None:
    # Steal all your data
    guild_id_prop: int=int(os.getenv('DISCORD_GUILD_ID_PROP'))
    guild_id_merp: int=int(os.getenv('DISCORD_GUILD_ID_MERP'))
    for guild in bot.guilds:
        get_cfg(guild)

    print(f'{bot.user.name}, rolling out in the age of {discord.__version__}!')

    with open('data/game.txt', 'r+', encoding='utf-8') as game_cfg:
        game=game_cfg.read()
        if game!='':
            await bot.change_presence(activity=discord.Game(game))
            print(f'Playing: {game}')

bot.add_cog(Fluff(bot))
bot.add_cog(Nerds(bot))
bot.add_cog(Queries(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
