from cogs.core import Core
from cogs.fluff import Fluff
from cogs.nerds import Nerds
from cogs.queries import Queries
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os

load_dotenv()

# if not os.path.exists('data/logs/'):
#     os.mkdir('data/logs/')
# 
# logger=logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler=logging.FileHandler(
#     filename=f'data/logs/{datetime.now().strftime("%Y-%m-%d")}.log',
#     encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter(
#     '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot: commands.Bot=commands.Bot(command_prefix=['Maia ', 'maia ', 'MAIA ',
    'Maia, ', 'maia, ', 'MAIA, '])

bot.add_cog(Core(bot))
bot.add_cog(Fluff(bot))
bot.add_cog(Nerds(bot))
bot.add_cog(Queries(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
