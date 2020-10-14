from cogs import get_cfg
from cogs.fluff import Fluff
from cogs.nerds import Nerds
from cogs.queries import Queries
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os

load_dotenv()

if not os.path.exists('data/logs/'):
    os.mkdir('data/logs/')

logger=logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler=logging.FileHandler(
    filename=f'data/logs/{datetime.now().strftime("%Y-%m-%d_%H%M%S")}.log',
    encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot: commands.Bot=commands.Bot(command_prefix=['Maia ', 'maia ', 'MAIA ',
    'Maia, ', 'maia, ', 'MAIA, '])

@bot.event
async def on_ready() -> None:
    for guild in bot.guilds:
        get_cfg(guild)

    print(f'{bot.user.name}, rolling out in the age of {discord.__version__}!')

    with open('data/game.txt', 'r+', encoding='utf-8') as game_cfg:
        game: str=game_cfg.read()
        if game!='':
            await bot.change_presence(activity=discord.Game(game))
            print(f'Playing: {game}')

bot.add_cog(Fluff(bot))
bot.add_cog(Nerds(bot))
bot.add_cog(Queries(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
